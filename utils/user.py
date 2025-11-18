"""
User class for storing demographic and experience data.
"""

class User:
    """
    Stores demographic and experience data for a user/rater.
    User ID is constructed from parent name initials, birthdate, birth year, and siblings.
    Formula: mother_initials + father_initials + (day+month) + (cross_sum_of_year * (siblings+1))
    """
    def __init__(self):
        self.user_id = ''
        self.data = {}  # Stores all questionnaire field responses
        # Legacy fields for backward compatibility
        self.gender = 'Not specified'
        self.age = 0
        self.nationality = ''
        self.player_exp = 0
        self.coach_exp = 0
        self.watch_exp = 0
        self.license = 'Not specified'
        # User ID components
        self.mother_initials = ''  # First two letters of mother's given name
        self.father_initials = ''  # First two letters of father's given name
        self.siblings = 0          # Number of siblings
        self.birth_day = 0         # Day of birth
        self.birth_month = 0       # Month of birth
        self.birth_year = 0        # Year of birth

    def _calculate_cross_sum(self, number):
        """Calculate the cross sum (sum of digits) of a number."""
        return sum(int(digit) for digit in str(abs(number)))

    def set_user_id(self):
        """
        Generate user_id from components.
        Format: mother_initials + father_initials + (day+month) + (cross_sum_year * (siblings+1))
        """
        if not self.mother_initials or not self.father_initials:
            self.user_id = 'unknown'
            return

        # Calculate day+month sum
        date_sum = self.birth_day + self.birth_month

        # Calculate cross sum of birth year
        year_cross_sum = self._calculate_cross_sum(self.birth_year)

        # Calculate final component: cross_sum * (siblings + 1)
        sibling_factor = year_cross_sum * (self.siblings + 1)

        # Concatenate all parts
        self.user_id = f"{self.mother_initials}{self.father_initials}{date_sum}{sibling_factor}"

    def set_field_value(self, field_name, value):
        """Set the value for a specific field and update User object."""
        self.data[field_name] = value

        # Update legacy fields for backward compatibility
        if field_name == 'gender':
            self.gender = value
        elif field_name == 'age':
            self.age = int(value) if value else 0
        elif field_name == 'nationality':
            self.nationality = value
        elif field_name == 'player_exp':
            self.player_exp = int(value) if value else 0
        elif field_name == 'coach_exp':
            self.coach_exp = int(value) if value else 0
        elif field_name == 'watch_exp':
            self.watch_exp = int(value) if value else 0
        elif field_name == 'license':
            self.license = value
        elif field_name == 'mother_initials':
            self.mother_initials = value[:2].lower() if value else ''
            self.set_user_id()
        elif field_name == 'father_initials':
            self.father_initials = value[:2].lower() if value else ''
            self.set_user_id()
        elif field_name == 'siblings':
            try:
                self.siblings = int(value) if value else 0
            except ValueError:
                self.siblings = 0
            self.set_user_id()
        elif field_name == 'birth_day':
            try:
                self.birth_day = int(value) if value else 0
            except ValueError:
                self.birth_day = 0
            self.set_user_id()
        elif field_name == 'birth_month':
            try:
                self.birth_month = int(value) if value else 0
            except ValueError:
                self.birth_month = 0
            self.set_user_id()
        elif field_name == 'birth_year':
            try:
                self.birth_year = int(value) if value else 0
            except ValueError:
                self.birth_year = 0
            self.set_user_id()

    def to_dict(self):
        """Convert user data to dictionary for JSON export."""
        from datetime import datetime
        return {
            'user_id': self.user_id,
            'gender': self.gender,
            'age': self.age,
            'nationality': self.nationality,
            'license': self.license,
            'player_exp': self.player_exp,
            'coach_exp': self.coach_exp,
            'watch_exp': self.watch_exp,
            'saved_at': datetime.now().isoformat(timespec='seconds'),
            **self.data
        }
