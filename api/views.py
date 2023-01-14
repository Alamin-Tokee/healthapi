from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializers import UserSerializer, UserLoginSerializer,PostPackagePlanSerializer, UserLogoutSerializer, GetPackagePlanSerializer, UpdatePackagePlanSerializer, DeletePackagePlanSerializer, PostPhoneNumberSerializer, GetPhoneNumberSerializer, PutPhoneNumberSerializer, DeletePhoneNumberSerializer, PatchPackagePlanSerializer, GetAddPaymentSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from .models import PlanChoices, PhoneNumber

# Create your views here.


class UserRegistration(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSiginin(APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)




class UserSignout(APIView):

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



class GetPackagePlan(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            raise Http404

    def get_plan_object(self, user):
        try:
            return PlanChoices.objects.get(user=user)
        except PlanChoices.DoesNotExist:
            raise Http404

    def post(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        user_dic = {'user':user.username}
        serializer = PostPackagePlanSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        print(user)
        user_dic = {'user' : user.username}
        print(user_dic)
        serializer = GetPackagePlanSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        # print(user)
        plan = self.get_plan_object(user)
        # print(plan.number)
        print(plan.id)
        context = {'user': user.username, 'plan_id':plan.number}
        serializer_class = PatchPackagePlanSerializer(instance=plan, data=request.data, context = context )
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def put(self, request, pk, *args, **kwargs):
        # print(request.data)
        user = self.get_object(pk)
        # print(user)
        plan = self.get_plan_object(user)
        print(plan.number)
        context = {'user': user.username}
        serializer_class = UpdatePackagePlanSerializer(instance=plan, data=request.data, context = context )
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        print(user)
        user_dic = {'user' : user.username}
        print(user_dic)
        plan = self.get_plan_object(user)
        serializer = DeletePackagePlanSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            plan.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddPhoneNumber(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            raise Http404

    def get_phone_object(self, ph):
        try:
            return PhoneNumber.objects.get(phone_id = ph)
        except PhoneNumber.DoesNotExist:
            raise Http404
    

    def post(self, request, pk, *arges, **kwargs):
        user = self.get_object(pk)
        context = {'user': user.username}
        serializer_class = PostPhoneNumberSerializer(data=request.data, context = context )
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk, *arges, **kwargs):
        user = self.get_object(pk)
        print(user)
        user_dic = {'user' : user.username}
        print(user_dic)
        serializer = GetPhoneNumberSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk, ph, *arges, **kwargs):
        user = self.get_object(pk)
        context = {'user': user.username}
        number = self.get_phone_object(ph)
        serializer_class = PutPhoneNumberSerializer(instance = number, data=request.data, context = context )
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, ph, *arges, **kwargs):
        user = self.get_object(pk)
        print(user)
        number = self.get_phone_object(ph)
        user_dic = {'user' : user.username, 'number':number.phone_id}
        serializer = DeletePhoneNumberSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            number.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddpaymentForPackage(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            raise Http404

    def get_plan_object(self, pid):
        try:
            return PlanChoices.objects.get(phone_id = pid)
        except PhoneNumber.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        # print(user)
        # plan = self.get_plan_object(pid)
        user_dic = {'user' : user.username}
        serializer = GetAddPaymentSerializer(data=request.data, context = user_dic)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


