
"""
用來表述你的 model 給 View Set
Serializing is changing the data from complex querysets from the DB to a form of data we can understand, like JSON or XML. 
Deserializing is reverting this process after validating the data we want to save to the DB.
"""
from rest_framework import serializers
from .models import Host

class HostSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # For the most part, any changes you make in your model should be reflected in your serializers too.
    creater = serializers.ReadOnlyField(source='creater.username')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Host
        fields = ('__all__') #('id', 'name', 'year_of_release')
        #read_only_fields = ('date_created', 'date_modified')
        #extra_kwargs = {'id': {'read_only': True}}