from rest_framework import serializers

class BaseCafeteriaSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.non_edit = ['id']
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        for key in self.non_edit:
            try:
                del validated_data[key]
            except KeyError:
                pass
        return super().update(instance, validated_data)