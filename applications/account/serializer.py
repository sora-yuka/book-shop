from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from applications.account.send_mail import send_confirmation_email, send_message

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    
    #* Класс сериализатор регистрации пользователя    
    password_confirm = serializers.CharField(
        min_length=6,
        write_only=True,
        required=True,
        )
    
    class Meta:
        model = User
        fields = '__all__'
        
    
    def validate(self, attrs):
        # проверка пароля
        
        pr = attrs.get('password')
        ps = attrs.pop('password_confirm')
        
        if pr != ps:
            raise serializers.ValidationError('Пароли не совпадают!')
        
        return attrs
    
    def create(self, validated_data):
        # создание и подтверждения пользователя
        
        user = User.objects.create_user(**validated_data)
        

        code = user.activation_code
        send_confirmation_email(user.email, code)
        
        return user
        

class LoginSerializer(serializers.Serializer):
    #* класс сериализатор логина пользователя
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    #! проверка почты и пароля пользователя

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email,
                            password=password)
        if not user:
            raise serializers.ValidationError('Неверный email или пароль')
        attrs['user'] = user
        return attrs
    

class ChangePasswordSerializer(serializers.Serializer):
    # класс сериализатор смены пароля пользователя
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6,)
    new_password_confirm = serializers.CharField(required=True, min_length=6)
    
    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('new_password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs
        
    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        
        if not user.check_password(old_password):
            raise serializers.ValidationError('Неверный пароль!')
        
        return old_password
    
    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()