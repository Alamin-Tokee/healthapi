# healthapi


## API endpoint description
1. Signup:  http://127.0.0.1:8000/api/signup/  
-> Request parameter(POST)  
email: example@gmail.com  
username: given number  
password : ******  

2. Signin: http://127.0.0.1:8000/api/signin/  
-> Request perameter(POST)  
username or email : both are work for login  
password : ********  

3. PackagePlan Add : http://127.0.0.1:8000/api/plan/{username}/  
-> Request perameter(POST)  
number: Usernumber which need to added to package  
plan: Gold 

4. PackagePlan Update : http://127.0.0.1:8000/api/plan/{username}/  
-> Request perameter(PUT)  
plan: Gold  

4. PackagePlan Number Update : http://127.0.0.1:8000/api/plan/{username}/  
-> Request perameter(PATCH)  
Contact: your number which you want to add new plan  


5. PackagePlan Get: http://127.0.0.1:8000/api/plan/{username}/  
-> Request perameter(GET)  


5. PackagePlan DELETE: http://127.0.0.1:8000/api/plan/{username}/  
-> Request perameter(DELETE)  


6. Add number: http://127.0.0.1:8000/api/phone/{username}/  
-> Request perameter(POST)  
contact: add number which you want to use for plan  
primary_number: True or False add for confirm using current plan  

7. Add number: http://127.0.0.1:8000/api/phone/{username}/  
-> Request perameter(PUT)    
contact: add number which you want to use for plan    
primary_number: True or False add for confirm using current plan    

8. Get active number: http://127.0.0.1:8000/api/phone/{username}/    
-> Request perameter(GET)  

9. Delete active number: http://127.0.0.1:8000/api/phone/{username}/    
-> Request perameter(DELETE)  

10. Get Payment: http://127.0.0.1:8000/api/payment/{username}/    
-> Request perameter(GET)    
This information mainly which you have to payment for further use and after that will be   payment   