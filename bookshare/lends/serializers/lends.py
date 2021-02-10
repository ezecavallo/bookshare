"""Lends serializers."""

# REST Framework
from rest_framework import serializers

# Models
from bookshare.lends.models import Lend, Book
from bookshare.circles.models import Membership

# Utils
from django.core.exceptions import ObjectDoesNotExist


class LendModelSerializer(serializers.ModelSerializer):

    book = serializers.StringRelatedField()
    lended_by = serializers.StringRelatedField()
    circle = serializers.StringRelatedField()

    class Meta:
        model = Lend
        fields = '__all__'

        read_only_fields = [
        'circle',
        'taked_by',
        'returned_at',
        'returned',
        'taked',
        'lended_by'
        ]

class CreateLendSerializer(serializers.ModelSerializer):

    lended_by = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Lend
        fields = [
            'lended_by',
            'book',
            'comments',
        ]

    def __init__(self, *args, **kwargs):
        super(CreateLendSerializer, self).__init__(*args, **kwargs)
        self.user = self.context['request'].user
        self.fields['book'] = serializers.SlugRelatedField(
            queryset=Book.objects.filter(owner=self.user),
            slug_field='title',
        )

    def validate_book(self, data):
        """Validate if book exists."""

        print(data)

        return data

    def validate(self, data):
        """Validate if is al lend in the circle already."""

        self.circle = self.context['circle']

        lend = Lend.objects.filter(
            circle=self.circle,
            lended_by=data['lended_by'],
            book=data['book']
        )
        if lend.exists():
            raise serializers.ValidationError('You have this book published in the circle.')

        return data

    def create(self, validated_data):

        lend = Lend.objects.create(**validated_data, circle=self.circle)

        # Update stats

        lended_by = Membership.objects.get(
            user=validated_data['lended_by'],
            circle=self.circle,
            is_active=True
        )
        lended_by.lends_offered += 1
        lended_by.save()

        self.circle.lends_offered += 1
        self.circle.save()

        return lend



class EndLendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lend
        fields = ['returned']

    def update(self, instance, validated_data):

        instance.returned = True
        instance.save()

        return instance


class TakeLendSerializer(serializers.ModelSerializer):

    class Meta:

        model = Lend
        fields = ['taked_by']

    def validate_taked_by(self, data):
        """Verify if user is in the circle."""

        try:
            member = Membership.objects.filter(
                circle=self.context['circle'],
                user=data
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not in the circle')

        self.member = member

        return data

    def validate(self, data):
        """Validate if the book was not taked."""

        lend = self.context['lend']
        if lend.taked is True:
            raise serializers.ValidationError('This lend was already taked.')

        return data

    def update(self, instance, validated_data):

        instance.taked_by = validated_data['taked_by']
        instance.taked = True

        # Update stats
        self.member.lends_taked += 1
        self.member.save()

        circle = self.context['circle']
        circle.lends_taked += 1
        circle.save()

        return instance
