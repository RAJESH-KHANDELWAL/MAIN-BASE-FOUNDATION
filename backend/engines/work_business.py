from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from backend.engines.base import BaseEngine


class WorkStatus(str, Enum):
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DELIVERED = "DELIVERED"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    HELD = "HELD"
    RELEASED = "RELEASED"
    REFUNDED = "REFUNDED"


@dataclass
class WorkRequest:
    work_id: str
    client_id: str
    title: str
    description: str
    budget: float
    currency: str = "INR"
    status: WorkStatus = WorkStatus.DRAFT
    freelancer_id: Optional[str] = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class WorkAssignment:
    work_id: str
    freelancer_id: str
    ai_assist_allowed: bool = True
    human_review_required: bool = True
    assigned_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class PaymentRecord:
    payment_id: str
    work_id: str
    client_id: str
    gross_amount: float
    platform_fee: float
    freelancer_amount: float
    currency: str = "INR"
    status: PaymentStatus = PaymentStatus.PENDING


class WorkBusinessEngine(BaseEngine):

    def __init__(self, platform_fee_rate: float = 0.10):
        super().__init__("WORK_BUSINESS_ENGINE")

        if not 0 <= platform_fee_rate < 1:
            raise ValueError(
                "platform_fee_rate must be between 0 and 1."
            )

        self.platform_fee_rate = platform_fee_rate
        self.work_requests: Dict[str, WorkRequest] = {}
        self.assignments: Dict[str, WorkAssignment] = {}
        self.payments: Dict[str, PaymentRecord] = {}

    def create_work(
        self,
        work_id: str,
        client_id: str,
        title: str,
        description: str,
        budget: float,
        currency: str = "INR",
    ) -> WorkRequest:

        if work_id in self.work_requests:
            raise ValueError("work_id already exists.")

        if not client_id.strip():
            raise ValueError("client_id is required.")

        if not title.strip():
            raise ValueError("title is required.")

        if budget <= 0:
            raise ValueError(
                "budget must be greater than zero."
            )

        work = WorkRequest(
            work_id=work_id,
            client_id=client_id,
            title=title,
            description=description,
            budget=budget,
            currency=currency,
            status=WorkStatus.POSTED,
        )

        self.work_requests[work_id] = work
        return work

    def assign_freelancer(
        self,
        work_id: str,
        freelancer_id: str,
        *,
        ai_assist_allowed: bool = True,
        human_review_required: bool = True,
    ) -> WorkAssignment:

        work = self._get_work(work_id)

        if work.status not in {
            WorkStatus.POSTED,
            WorkStatus.ASSIGNED,
        }:
            raise ValueError(
                "Work is not available for assignment."
            )

        if not freelancer_id.strip():
            raise ValueError(
                "freelancer_id is required."
            )

        assignment = WorkAssignment(
            work_id=work_id,
            freelancer_id=freelancer_id,
            ai_assist_allowed=ai_assist_allowed,
            human_review_required=human_review_required,
        )

        self.assignments[work_id] = assignment
        work.freelancer_id = freelancer_id
        work.status = WorkStatus.ASSIGNED

        return assignment

    def start_work(
        self,
        work_id: str,
    ) -> WorkRequest:

        work = self._get_work(work_id)

        if work_id not in self.assignments:
            raise ValueError(
                "A freelancer must be assigned before work starts."
            )

        work.status = WorkStatus.IN_PROGRESS
        return work

    def submit_for_review(
        self,
        work_id: str,
    ) -> WorkRequest:

        work = self._get_work(work_id)

        if work.status != WorkStatus.IN_PROGRESS:
            raise ValueError(
                "Only in-progress work can enter review."
            )

        work.status = WorkStatus.REVIEW
        return work

    def deliver(
        self,
        work_id: str,
    ) -> WorkRequest:

        work = self._get_work(work_id)

        if work.status != WorkStatus.REVIEW:
            raise ValueError(
                "Work must pass review before delivery."
            )

        work.status = WorkStatus.DELIVERED
        return work

    def approve(
        self,
        work_id: str,
    ) -> WorkRequest:

        work = self._get_work(work_id)

        if work.status != WorkStatus.DELIVERED:
            raise ValueError(
                "Only delivered work can be approved."
            )

        work.status = WorkStatus.APPROVED
        return work

    def create_payment(
        self,
        payment_id: str,
        work_id: str,
    ) -> PaymentRecord:

        if payment_id in self.payments:
            raise ValueError(
                "payment_id already exists."
            )

        work = self._get_work(work_id)

        if work.freelancer_id is None:
            raise ValueError(
                "A freelancer must be assigned before payment."
            )

        platform_fee = round(
            work.budget * self.platform_fee_rate,
            2,
        )

        freelancer_amount = round(
            work.budget - platform_fee,
            2,
        )

        payment = PaymentRecord(
            payment_id=payment_id,
            work_id=work_id,
            client_id=work.client_id,
            gross_amount=work.budget,
            platform_fee=platform_fee,
            freelancer_amount=freelancer_amount,
            currency=work.currency,
        )

        self.payments[payment_id] = payment
        return payment

    def authorize_payment(
        self,
        payment_id: str,
    ) -> PaymentRecord:

        payment = self._get_payment(payment_id)

        if payment.status != PaymentStatus.PENDING:
            raise ValueError(
                "Only pending payments can be authorized."
            )

        payment.status = PaymentStatus.AUTHORIZED
        return payment

    def mark_payment_held(
        self,
        payment_id: str,
    ) -> PaymentRecord:

        payment = self._get_payment(payment_id)

        if payment.status not in {
            PaymentStatus.PENDING,
            PaymentStatus.AUTHORIZED,
        }:
            raise ValueError(
                "Payment cannot be moved to HELD."
            )

        payment.status = PaymentStatus.HELD
        return payment

    def release_payment(
        self,
        payment_id: str,
    ) -> PaymentRecord:

        payment = self._get_payment(payment_id)
        work = self._get_work(payment.work_id)

        if work.status != WorkStatus.APPROVED:
            raise ValueError(
                "Payment can be released only after approval."
            )

        if payment.status != PaymentStatus.HELD:
            raise ValueError(
                "Payment must be HELD before release."
            )

        payment.status = PaymentStatus.RELEASED
        return payment

    def get_work(
        self,
        work_id: str,
    ) -> Optional[WorkRequest]:

        return self.work_requests.get(work_id)

    def list_work(
        self,
    ) -> List[WorkRequest]:

        return list(
            self.work_requests.values()
        )

    def status(
        self,
    ) -> dict:

        return {
            "engine": self.name,
            "state": self.state,
            "work_count": len(self.work_requests),
            "assignment_count": len(self.assignments),
            "payment_count": len(self.payments),
            "platform_fee_rate": self.platform_fee_rate,
        }

    def _get_work(
        self,
        work_id: str,
    ) -> WorkRequest:

        work = self.work_requests.get(work_id)

        if work is None:
            raise KeyError(
                f"Unknown work_id: {work_id}"
            )

        return work

    def _get_payment(
        self,
        payment_id: str,
    ) -> PaymentRecord:

        payment = self.payments.get(payment_id)

        if payment is None:
            raise KeyError(
                f"Unknown payment_id: {payment_id}"
            )

        return payment


__all__ = [
    "WorkStatus",
    "PaymentStatus",
    "WorkRequest",
    "WorkAssignment",
    "PaymentRecord",
    "WorkBusinessEngine",
]
