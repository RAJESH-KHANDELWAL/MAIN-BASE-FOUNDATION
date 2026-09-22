import random
import string


class IdentityGenerator:

    LENGTH = 6
    UNIQUE_ID_LENGTH = 8

    @staticmethod
    def _generate(prefix: str):
        return prefix + "-" + "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=IdentityGenerator.LENGTH
            )
        )

    @staticmethod
    def generate_master_id():
        return IdentityGenerator._generate("MBF")

    @staticmethod
    def generate_identity_id():
        return IdentityGenerator._generate("IDT")

    @staticmethod
    def generate_supreme_id():
        return IdentityGenerator._generate("SUP")

    @staticmethod
    def generate_user_id():
        return IdentityGenerator._generate("USR")

    @staticmethod
    def generate_profile_id():
        return IdentityGenerator._generate("PRO")

    @staticmethod
    def generate_team_id():
        return IdentityGenerator._generate("TEM")

    @staticmethod
    def generate_organization_id():
        return IdentityGenerator._generate("ORG")

    @staticmethod
    def generate_business_id():
        return IdentityGenerator._generate("BUS")

    @staticmethod
    def generate_project_id():
        return IdentityGenerator._generate("PRJ")

    @staticmethod
    def generate_role_id():
        return IdentityGenerator._generate("ROL")

    @staticmethod
    def generate_permission_id():
        return IdentityGenerator._generate("PER")

    @staticmethod
    def generate_session_id():
        return IdentityGenerator._generate("SES")

    @staticmethod
    def generate_api_key():
        return IdentityGenerator._generate("API")

    @staticmethod
    def generate_token():
        return IdentityGenerator._generate("TOK")

    @staticmethod
    def generate_unique_id():
        """Generate an 8-character ecosystem-wide unique ID candidate."""

        return "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=IdentityGenerator.UNIQUE_ID_LENGTH
            )
        )
