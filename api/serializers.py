from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, UserInfo,PlanChoices,PhoneNumber
from django.core.exceptions import ValidationError
from uuid import uuid4


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=8)
    # password2 = serializers.CharField(max_length=8)


    def validate(self, data):
        user = data.get("username", None)

        try:
            if len(user) < 11:
                raise ValidationError("User name is not correct format")
        except Exception as e:
            raise ValidationError(str(e))

        
        return data


    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    usernumber = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        print(data)
        usernumber = data.get("usernumber", None)
        password = data.get("password", None)
        if not usernumber and not password:
            raise ValidationError("Details not entered.")
        # user = None
        # if the email has been passed
        if '@' in usernumber:
            user = User.objects.filter(
                Q(email=usernumber) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=usernumber)
        else:
            user = User.objects.filter(
                Q(username=usernumber) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=usernumber)
        
        user_info = UserInfo.objects.get(user=user)
        

        print(user_info)

        if user_info.if_logged:
            raise ValidationError("User already logged in.")
        user_info.if_logged = True
        data['token'] = uuid4()
        user_info.token = data['token']
        user_info.save()
        return data

    class Meta:
        model = User
        fields = (
            'usernumber',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = UserInfo.objects.get(token=token)
            if not user.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.if_logged = False
        user.token = "empty"
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )



# Serializer for packageplan

class PostPackagePlanSerializer(serializers.ModelSerializer):

    def validate(self, data):

        # print(instance)
        # print(validated_data)
        userid = self.context['user']
        # print(userid)
        number_id = data.get("number", None)
        # print(number_id.phone_id)
        plan = data.get("plan", None)
        # print(plan)

        user = User.objects.get(username = userid)
        planpackage = PlanChoices.objects.filter(user=user)
        print(planpackage)
        number = PhoneNumber.objects.get(phone_id = number_id.phone_id)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            # print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
            # number = PhoneNumber.objects.get(phone_id = number_id.phone_id)
            # print(number.primary_number)
            # if not number:
            #     raise ValidationError("This number is not exits")

            # if planpackage.number:
            #     raise ValidationError("Currently you use a plan, please update your plan")

        except Exception as e:
            raise ValidationError(str(e))


        number.primary_number = True
        number.save()

        data['user'] = userinfo.user
        data['number'] = number
        data['plan'] = plan
       
        return data

    class Meta:
        model = PlanChoices
        fields = ('number', 'plan')
        # fields = (
        #     'user',
        #     'number',
        #     'plan',
        #     'created_at',
        #     'updated_at',
        #     'status'
        # )


class GetPackagePlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, read_only=True)
    number = serializers.CharField(required=False, read_only=True)
    plan = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    updated_at = serializers.DateTimeField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)


    def validate(self, data):
        print(data)
        # userid = data.get("user", "alamin")
        userid = self.context['user']
        # print(user)
        # token = data.get("token", None)
        # user = None

        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))


        # username = userinfo.user.username
        # print(username)

        try:
            userplan = PlanChoices.objects.get(user=user)
            if not userplan:
                ValidationError("User has no plan.")
        except:
            raise ValidationError(str(e))

        
        print (userplan)

            
        data['user'] = userinfo.user.username
        data["number"] = userplan.number
        data["plan"] = userplan.plan
        data["created_at"] = userplan.created_at
        data["updated_at"] = userplan.updated_at 
        data['status'] = "User active plan gate succesfully"
        return data

    class Meta:
        model = PlanChoices
        fields = (
            'user',
            'number',
            'plan',
            'created_at',
            'updated_at',
            'status'
        )

class UpdatePackagePlanSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(required=False, read_only=True)
    # number = serializers.CharField(required=False, read_only=True)
    # plan = serializers.CharField(required=False, read_only=True)


    def update(self, instance, validated_data):

        # print(instance)
        # print(validated_data)
        userid = self.context['user']
        print(userid)
        # token = data.get("token", None)
        # user = None
        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))


        try:
            userplan = PlanChoices.objects.get(user=user)
            if not userplan:
                ValidationError("User has no plan.")
        except:
            raise ValidationError(str(e))    


        if userplan.plan == 'Bronze':
            print("You have bronze plan")
        elif userplan.plan == 'Silver':
            print("You have a silver plan")
        else:
            print("You have a gold plan")


        # instance.user = self.context['user']
        # instance.number = validated_data.get('number', instance.number)
        instance.plan = validated_data.get('plan', instance.plan)
        instance.save()
        return instance

    class Meta:
        model = PlanChoices
        fields = ('plan',)
        # fields = (
        #     'user',
        #     'number',
        #     'plan',
        #     'created_at',
        #     'updated_at',
        #     'status'
        # )




class PatchPackagePlanSerializer(serializers.ModelSerializer):


    def update(self, instance, validated_data):

        # print(instance)
        # print(validated_data)
        userid = self.context['user']
        print(userid)
        number = self.context['plan_id']
        print(number)
        # token = data.get("token", None)
        # user = None
        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
            userplan = PlanChoices.objects.get(user=user)
            if not userplan:
                raise ValidationError("User has no plan.First create a plan for use")

            if userplan.plan == 'Bronze' or userplan.plan == 'Silver':
                raise ValidationError("Your are not allowed to change the plan, beacause timeperiod is not end")
        except Exception as e:
            raise ValidationError(str(e))



        exit_number = PhoneNumber.objects.get(contact = userplan.number)
        # print(exit_number)
        exit_number.primary_number = False
        exit_number.save()

        present_number = PhoneNumber.objects.get(contact = number)
        userplan.number = present_number
        userplan.save()

        # instance.user = self.context['user']
        # instance.number = validated_data.get('number', instance.number)
        instance.contact = validated_data.get('number', instance.contact)
        instance.primary_number = validated_data.get('number', instance.primary_number)

        instance.save()
        return instance

    class Meta:
        model = PhoneNumber
        fields = ('contact','primary_number')
        # fields = (
        #     'user',
        #     'number',
        #     'plan',
        #     'created_at',
        #     'updated_at',
        #     'status'
        # )






class DeletePackagePlanSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
    
        # print(instance)
        # print(validated_data)
        userid = self.context['user']
        print(userid)
        # token = data.get("token", None)
        # user = None
        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))


        try:
            userplan = PlanChoices.objects.get(user=user)
            if not userplan:
                ValidationError("User has no plan.")

            if userplan.plan == "Bronze":
                ValidationError("Broneze, You are not allowed to delete this plan within this days")
            elif userplan.plan == "Silver":
                ValidationError("Silver, You are not allowed to delete this plan within this days")
        except:
            raise ValidationError(str(e))    

        data['status'] = 'Succefully deleted your plan'
       
        return data

    class Meta:
        model = PlanChoices
        fields = ('status',)


class PostPhoneNumberSerializer(serializers.ModelSerializer):

    def validate(self, data):
        print(data)
        # userid = data.get("user", "alamin")
        userid = self.context['user']
        # print(user)
        # token = data.get("token", None)
        # user = None
        contact = data.get("contact")
        primary_number = data.get("primary_number")

        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
            usernumber = PhoneNumber.objects.filter(contact=contact)
            if usernumber:
                raise ValidationError("This number is already added")
            
        except Exception as e:
            raise ValidationError(str(e))


        # username = userinfo.user.username
        # print(username)



        # try:
        #     userplan = PlanChoices.objects.get(user=user)
        #     if not userplan:
        #         ValidationError("User has no plan.")
        # except:
        #     raise ValidationError(str(e))

        
        # print (userplan)

            
        data['user'] = userinfo.user
        data["contact"] = contact
        data["primary_number"] = primary_number
        
        return data

    class Meta:
        model = PhoneNumber
        fields = ('contact', 'primary_number')



class GetPhoneNumberSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, read_only=True)
    contact = serializers.CharField(required=False, read_only=True)
    primary_number = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        print(data)
        # userid = data.get("user", "alamin")
        userid = self.context['user']
        # print(user)
        # token = data.get("token", None)
        # user = None

        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
            phoneuser = PhoneNumber.objects.get(user=user, primary_number=True)
            if phoneuser: 
                raise ValidationError("User dont have any phone number active phone number")
        except Exception as e:
            raise ValidationError(str(e))

        print(phoneuser.user)
            
            
        data['user'] = userinfo.user
        data["contact"] = phoneuser.contact
        data["primary_number"] = phoneuser.primary_number

        return data

    class Meta:
        model = PhoneNumber
        fields = '__all__'


class PutPhoneNumberSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        userid = self.context['user']
        # print(user)
        # token = data.get("token", None)
        # user = None

        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")

        except Exception as e:
            raise ValidationError(str(e))

        instance.contact = validated_data.get('contact', instance.contact)
        instance.primary_number = validated_data.get('primary_number', instance.primary_number)
        instance.save()

        return instance

    class Meta:
        model = PhoneNumber
        fields = ('contact', 'primary_number')



class DeletePhoneNumberSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
    
        # print(instance)
        # print(validated_data)
        userid = self.context['user']
        number = self.context['number']
        print(userid)
        # token = data.get("token", None)
        # user = None
        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")

            phone = PhoneNumber.objects.get(phone_id = number)

            if not phone or phone.primary_number == True:
                raise ValidationError("Your are not allowed to delete this number or does not exits this number")

            if phone.user != userinfo.user:
                raise ValidationError("It is not your number so you are not eligibe to delete this number")
        except Exception as e:
            raise ValidationError(str(e))


        data['status'] = 'Succefully deleted your phone number'
       
        return data

    class Meta:
        model = PlanChoices
        fields = ('status',)




class GetAddPaymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, read_only=True)
    number = serializers.CharField(required=False, read_only=True)
    plan = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    updated_at = serializers.DateTimeField(required=False, read_only=True)
    status = serializers.CharField(required=False, read_only=True)


    def validate(self, data):
        print(data)
        # userid = data.get("user", "alamin")
        userid = self.context['user']
        print(userid)
        # print(user)
        # token = data.get("token", None)
        # user = None

        user = User.objects.get(username = userid)
        
        try:
            userinfo = UserInfo.objects.get(user=user)
            print(userinfo)
            if not userinfo.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))


        # username = userinfo.user.username
        # print(username)

        try:
            userplan = PlanChoices.objects.get(user=user)
            if not userplan:
                ValidationError("User has no plan.")
        except:
            raise ValidationError(str(e))

        
        print (userplan)

            
        data['user'] = userinfo.user
        data["number"] = userplan.number
        data["plan"] = userplan.plan
        data["created_at"] = userplan.created_at
        data["updated_at"] = userplan.updated_at 
        data['status'] = "You have to pay this plan, please add your card here"
        return data

    class Meta:
        model = PlanChoices
        fields = (
            'user',
            'number',
            'plan',
            'created_at',
            'updated_at',
            'status'
        )