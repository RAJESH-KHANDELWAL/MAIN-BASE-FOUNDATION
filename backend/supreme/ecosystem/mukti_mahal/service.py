"""
MAIN BASE FOUNDATION

SUPREME — Mukti Mahal Service Layer

Central application service for the Mukti Mahal ecosystem.

Responsibilities:

- Mukti Mahal management
- Pratap Group management
- Family management
- Staff management
- Estate-area management
- Business-division management
- Executive-role management
- Capability evaluation
- Family succession / board learning
- Family visit workflow
- Mukti principles
- Runtime status

This service contains application state and business operations.

Sensitive credentials, passwords, OTPs and payment secrets
must never be stored here.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .model import (
    BusinessCapabilityEvaluation,
    BusinessDivision,
    BusinessExecutiveRole,
    EstateAreaType,
    FamilyGeneration,
    FamilyRole,
    MuktiMahal,
    MuktiMahalEstateArea,
    MuktiMahalFamilyMember,
    MuktiMahalFamilyVisit,
    MuktiMahalSetting,
    MuktiMahalStaffMember,
    MuktiPrinciples,
    PratapGroup,
    StaffType,
)


class MuktiMahalService:
    """Central service layer for the Mukti Mahal ecosystem."""

    def __init__(self) -> None:
        self._initialized: bool = False

        self._mahals: Dict[str, MuktiMahal] = {}

        self._groups: Dict[str, PratapGroup] = {}

        self._family_members: Dict[
            str, MuktiMahalFamilyMember
        ] = {}

        self._staff: Dict[
            str, MuktiMahalStaffMember
        ] = {}

        self._estate_areas: Dict[
            str, MuktiMahalEstateArea
        ] = {}

        self._capability_evaluations: Dict[
            str, BusinessCapabilityEvaluation
        ] = {}

        self._family_visits: Dict[
            str, MuktiMahalFamilyVisit
        ] = {}

        self._settings: Dict[
            str, MuktiMahalSetting
        ] = {}

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self) -> dict:
        """Initialize the service runtime."""

        self._initialized = True

        return self.status()

    # =====================================================
    # STATUS
    # =====================================================

    def status(self) -> dict:
        """Return a safe runtime status."""

        return {
            "service": "MUKTI_MAHAL",
            "initialized": self._initialized,
            "mahals": len(self._mahals),
            "groups": len(self._groups),
            "family_members": len(self._family_members),
            "staff_members": len(self._staff),
            "estate_areas": len(self._estate_areas),
            "capability_evaluations": len(
                self._capability_evaluations
            ),
            "family_visits": len(
                self._family_visits
            ),
            "settings": len(self._settings),
        }

    # =====================================================
    # MAHAL MANAGEMENT
    # =====================================================

    def create_mahal(
        self,
        mahal: MuktiMahal,
    ) -> MuktiMahal:
        """Create or register a Mahal."""

        if mahal.mahal_id in self._mahals:
            raise ValueError(
                "Mahal already exists."
            )

        self._mahals[
            mahal.mahal_id
        ] = mahal

        return mahal

    def get_mahal(
        self,
        mahal_id: str,
    ) -> Optional[MuktiMahal]:
        """Get a Mahal by ID."""

        return self._mahals.get(
            mahal_id
        )

    def list_mahals(
        self,
    ) -> List[MuktiMahal]:
        """List all Mahals."""

        return list(
            self._mahals.values()
        )

    # =====================================================
    # PRATAP GROUP
    # =====================================================

    def create_group(
        self,
        group: PratapGroup,
    ) -> PratapGroup:
        """Create or register a business group."""

        if group.group_id in self._groups:
            raise ValueError(
                "Business group already exists."
            )

        self._groups[
            group.group_id
        ] = group

        return group

    def get_group(
        self,
        group_id: str,
    ) -> Optional[PratapGroup]:
        """Get a business group."""

        return self._groups.get(
            group_id
        )

    def list_groups(
        self,
    ) -> List[PratapGroup]:
        """List all business groups."""

        return list(
            self._groups.values()
        )

    def add_business_division(
        self,
        group_id: str,
        division: BusinessDivision,
    ) -> PratapGroup:
        """Add a business division to a group."""

        group = self.get_group(
            group_id
        )

        if group is None:
            raise ValueError(
                "Business group not found."
            )

        if division not in group.business_divisions:
            group.business_divisions.append(
                division
            )

        return group

    # =====================================================
    # FAMILY MANAGEMENT
    # =====================================================

    def add_family_member(
        self,
        member: MuktiMahalFamilyMember,
        mahal_id: Optional[str] = None,
    ) -> MuktiMahalFamilyMember:
        """Add a family member."""

        if member.character_id in self._family_members:
            raise ValueError(
                "Family member already exists."
            )

        if mahal_id is not None:
            mahal = self.get_mahal(
                mahal_id
            )

            if mahal is None:
                raise ValueError(
                    "Mahal not found."
                )

            if (
                member.character_id
                not in mahal.family_member_ids
            ):
                mahal.family_member_ids.append(
                    member.character_id
                )

        self._family_members[
            member.character_id
        ] = member

        return member

    def get_family_member(
        self,
        character_id: str,
    ) -> Optional[MuktiMahalFamilyMember]:
        """Get a family member."""

        return self._family_members.get(
            character_id
        )

    def list_family_members(
        self,
        generation: Optional[
            FamilyGeneration
        ] = None,
        family_role: Optional[
            FamilyRole
        ] = None,
    ) -> List[MuktiMahalFamilyMember]:
        """List family members with optional filters."""

        members = list(
            self._family_members.values()
        )

        if generation is not None:
            members = [
                member
                for member in members
                if member.generation == generation
            ]

        if family_role is not None:
            members = [
                member
                for member in members
                if member.family_role == family_role
            ]

        return members

    # =====================================================
    # STAFF MANAGEMENT
    # =====================================================

    def add_staff_member(
        self,
        staff: MuktiMahalStaffMember,
        mahal_id: Optional[str] = None,
    ) -> MuktiMahalStaffMember:
        """Add a staff member."""

        if staff.staff_id in self._staff:
            raise ValueError(
                "Staff member already exists."
            )

        if mahal_id is not None:
            mahal = self.get_mahal(
                mahal_id
            )

            if mahal is None:
                raise ValueError(
                    "Mahal not found."
                )

            if (
                staff.staff_id
                not in mahal.staff_member_ids
            ):
                mahal.staff_member_ids.append(
                    staff.staff_id
                )

        self._staff[
            staff.staff_id
        ] = staff

        return staff

    def get_staff(
        self,
        staff_id: str,
    ) -> Optional[MuktiMahalStaffMember]:
        """Get staff by ID."""

        return self._staff.get(
            staff_id
        )

    def list_staff(
        self,
        staff_type: Optional[StaffType] = None,
    ) -> List[MuktiMahalStaffMember]:
        """List staff with an optional staff-type filter."""

        staff_members = list(
            self._staff.values()
        )

        if staff_type is not None:
            staff_members = [
                staff
                for staff in staff_members
                if staff.staff_type == staff_type
            ]

        return staff_members

    # =====================================================
    # ESTATE MANAGEMENT
    # =====================================================

    def add_estate_area(
        self,
        area: MuktiMahalEstateArea,
        mahal_id: Optional[str] = None,
    ) -> MuktiMahalEstateArea:
        """Add an estate area."""

        if area.area_id in self._estate_areas:
            raise ValueError(
                "Estate area already exists."
            )

        if mahal_id is not None:
            mahal = self.get_mahal(
                mahal_id
            )

            if mahal is None:
                raise ValueError(
                    "Mahal not found."
                )

            if (
                area.area_id
                not in mahal.estate_area_ids
            ):
                mahal.estate_area_ids.append(
                    area.area_id
                )

        self._estate_areas[
            area.area_id
        ] = area

        return area

    def get_estate_area(
        self,
        area_id: str,
    ) -> Optional[MuktiMahalEstateArea]:
        """Get an estate area."""

        return self._estate_areas.get(
            area_id
        )

    def list_estate_areas(
        self,
        area_type: Optional[
            EstateAreaType
        ] = None,
        floor: Optional[int] = None,
    ) -> List[MuktiMahalEstateArea]:
        """List estate areas with optional filters."""

        areas = list(
            self._estate_areas.values()
        )

        if area_type is not None:
            areas = [
                area
                for area in areas
                if area.area_type == area_type
            ]

        if floor is not None:
            areas = [
                area
                for area in areas
                if area.floor == floor
            ]

        return areas

    # =====================================================
    # EXECUTIVE ROLE
    # =====================================================

    def assign_executive_role(
        self,
        character_id: str,
        role: BusinessExecutiveRole,
    ) -> MuktiMahalFamilyMember:
        """
        Assign an executive role.

        Senior responsibility should be based on
        capability and governance rules rather than
        family membership alone.
        """

        member = self.get_family_member(
            character_id
        )

        if member is None:
            raise ValueError(
                "Family member not found."
            )

        if not member.capability_proven:
            raise ValueError(
                "Capability has not been proven."
            )

        member.executive_role = role

        return member

    # =====================================================
    # CAPABILITY EVALUATION
    # =====================================================

    def register_capability_evaluation(
        self,
        evaluation: BusinessCapabilityEvaluation,
    ) -> BusinessCapabilityEvaluation:
        """Register a capability evaluation."""

        if (
            evaluation.evaluation_id
            in self._capability_evaluations
        ):
            raise ValueError(
                "Capability evaluation already exists."
            )

        member = self.get_family_member(
            evaluation.character_id
        )

        if member is None:
            raise ValueError(
                "Family member not found."
            )

        self._capability_evaluations[
            evaluation.evaluation_id
        ] = evaluation

        return evaluation

    def get_capability_evaluation(
        self,
        evaluation_id: str,
    ) -> Optional[
        BusinessCapabilityEvaluation
    ]:
        """Get a capability evaluation."""

        return self._capability_evaluations.get(
            evaluation_id
        )

    def list_capability_evaluations(
        self,
        character_id: Optional[str] = None,
    ) -> List[
        BusinessCapabilityEvaluation
    ]:
        """List capability evaluations."""

        evaluations = list(
            self._capability_evaluations.values()
        )

        if character_id is not None:
            evaluations = [
                evaluation
                for evaluation in evaluations
                if evaluation.character_id == character_id
            ]

        return evaluations

    def qualify_executive_role(
        self,
        character_id: str,
        role: BusinessExecutiveRole,
    ) -> MuktiMahalFamilyMember:
        """
        Qualify a family member for an executive role
        after capability has been proven.
        """

        member = self.get_family_member(
            character_id
        )

        if member is None:
            raise ValueError(
                "Family member not found."
            )

        evaluations = (
            self.list_capability_evaluations(
                character_id=character_id
            )
        )

        if not evaluations:
            raise ValueError(
                "No capability evaluation found."
            )

        proven = any(
            evaluation.overall_qualified
            for evaluation in evaluations
        )

        if not proven:
            raise ValueError(
                "Capability requirements have not been met."
            )

        member.capability_proven = True
        member.executive_role = role

        return member

    # =====================================================
    # FAMILY VISIT
    # =====================================================

    def register_family_visit(
        self,
        visit: MuktiMahalFamilyVisit,
    ) -> MuktiMahalFamilyVisit:
        """Register a family visit."""

        if (
            visit.visit_id
            in self._family_visits
        ):
            raise ValueError(
                "Family visit already exists."
            )

        self._family_visits[
            visit.visit_id
        ] = visit

        return visit

    def get_family_visit(
        self,
        visit_id: str,
    ) -> Optional[MuktiMahalFamilyVisit]:
        """Get a family visit."""

        return self._family_visits.get(
            visit_id
        )

    def list_family_visits(
        self,
    ) -> List[MuktiMahalFamilyVisit]:
        """List family visits."""

        return list(
            self._family_visits.values()
        )

    def complete_welcome(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the welcome stage."""

        visit = self._require_visit(
            visit_id
        )

        visit.welcome_completed = True

        return visit

    def complete_introductions(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete introductions."""

        visit = self._require_visit(
            visit_id
        )

        if not visit.welcome_completed:
            raise ValueError(
                "Welcome must be completed first."
            )

        visit.introductions_completed = True

        return visit

    def complete_dinner(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the dinner stage."""

        visit = self._require_visit(
            visit_id
        )

        if not visit.introductions_completed:
            raise ValueError(
                "Introductions must be completed first."
            )

        visit.dinner_completed = True

        return visit

    def complete_business_discussion(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Complete the business discussion."""

        visit = self._require_visit(
            visit_id
        )

        if not visit.dinner_completed:
            raise ValueError(
                "Dinner must be completed first."
            )

        visit.business_discussion_completed = True
        visit.completed = True

        return visit

    def _require_visit(
        self,
        visit_id: str,
    ) -> MuktiMahalFamilyVisit:
        """Return a visit or raise a clear error."""

        visit = self.get_family_visit(
            visit_id
        )

        if visit is None:
            raise ValueError(
                "Family visit not found."
            )

        return visit

    # =====================================================
    # MUKTI PRINCIPLES
    # =====================================================

    def principles(self) -> MuktiPrinciples:
        """Return the configured Mukti principles."""

        return MuktiPrinciples()

    # =====================================================
    # SETTINGS
    # =====================================================

    def set_setting(
        self,
        setting: MuktiMahalSetting,
    ) -> MuktiMahalSetting:
        """Create or update a Mahal setting."""

        self._settings[
            setting.setting_id
        ] = setting

        return setting

    def get_setting(
        self,
        setting_id: str,
    ) -> Optional[MuktiMahalSetting]:
        """Get a Mahal setting."""

        return self._settings.get(
            setting_id
        )

    def list_settings(
        self,
    ) -> List[MuktiMahalSetting]:
        """List configured settings."""

        return list(
            self._settings.values()
        )


__all__ = [
    "MuktiMahalService",
]
