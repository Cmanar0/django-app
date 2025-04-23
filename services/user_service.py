from authentication.models import UserProfile
from services.email_service import update_user_in_brevo_list

def update_user_profile(user, data):
    """
    Update a user's profile with the provided data and sync to Brevo.
    
    Args:
        user: The user object
        data: Dictionary containing profile data
        
    Returns:
        The updated user profile
    """
    profile = user.userprofile
    
    # Update profile fields
    profile.first_name = data.get('first_name', '')
    profile.last_name = data.get('last_name', '')
    profile.company_name = data.get('company_name', '')
    profile.phone = data.get('phone', '')
    profile.linkedin = data.get('linkedin', '')
    profile.website = data.get('website', '')
    profile.instagram = data.get('instagram', '')
    profile.street = data.get('street', '')
    profile.city = data.get('city', '')
    profile.country = data.get('country', '')
    profile.membership_program = data.get('membership_program', 'member')
    profile.payment_type = data.get('payment_type', '')
    
    # Save the profile
    profile.save()
    
    # Sync to Brevo
    update_user_in_brevo_list(
        email=user.email,
        first_name=profile.first_name,
        last_name=profile.last_name,
        company_name=profile.company_name,
        phone=profile.phone,
        membership_program=profile.get_membership_program_display(),
        payment_type=profile.get_payment_type_display() or '',
        verified=profile.is_email_verified
    )
    
    return profile 