from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FoodTruck


class FoodTruckOwnerRegistrationForm(UserCreationForm):
    """
    Registration form for food truck owners.
    Extends UserCreationForm to include additional fields for food truck owners.
    """
    
    # Additional user fields
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text='Optional. Your contact phone number.'
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Optional. Your business address.'
    )
    
    # Food truck information
    truck_name = forms.CharField(
        max_length=100,
        required=False,
        help_text='Optional. Name of your food truck (you can add this later).',
        label='Food Truck Name'
    )
    
    truck_city = forms.CharField(
        max_length=50,
        required=False,
        help_text='Optional. City where your food truck operates.',
        label='Operating City'
    )
    
    truck_cuisine = forms.CharField(
        max_length=50,
        required=False,
        help_text='Optional. Type of cuisine your truck serves.',
        label='Cuisine Type'
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['truck_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['truck_city'].widget.attrs.update({'class': 'form-control'})
        self.fields['truck_cuisine'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        """
        Save the user with food_truck_owner role and create food truck if provided.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.role = 'food_truck_owner'  # Set the role to food truck owner
        
        if commit:
            user.save()
            
            # Create food truck if truck name is provided
            truck_name = self.cleaned_data.get('truck_name')
            if truck_name:
                truck_city = self.cleaned_data.get('truck_city', '')
                truck_cuisine = self.cleaned_data.get('truck_cuisine', '')
                
                FoodTruck.objects.create(
                    name=truck_name,
                    city=truck_city,
                    cuisine=truck_cuisine
                )
        
        return user