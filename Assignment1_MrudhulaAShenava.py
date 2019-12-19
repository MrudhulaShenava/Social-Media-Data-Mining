#class initialization
class University:
#__init__() function initilization to assign values to object property
   def __init__(type, course, standing, year):
       type.course = course
       type.standing = standing
       type.year = year
u1 = University("Engineering", "Sophomore", 2019)
print(u1.course)
print(u1.standing)
print(u1.year)
#function declaration with default parameter value
print("\n")
print("Function declaration with default values \n")
def dogs(breed = "beagle"):
    print("This dog is a " + breed)
dogs("German Sheperd")
dogs()
dogs("husky")
print("\n")
print("List Comprehension")
print("------------------")
celcius = [37.1, 0, 52, 100, 23.5, 10.1]
print("Current List : ", celcius)
celcius.extend([-10, 3, -1])
print("Extended List : ", celcius)
ferenheit = [((float(9)/5) * x + 32) for x in celcius]
print(celcius)
print(ferenheit)
print("\n")
print("Dictionary comprehension")
print("------------------------")
keys=[1,2,3,4,5,6,7,8]
values=['Loons', 'Owl', 'Parrot', 'Sparrow', 'Woodpecker', 'Eagle', 'Hummingbird', 'Goose']
dict_comp = {k:v for (k,v)in zip(keys, values)}
rev_dict = {v:k for (k,v) in zip(keys, values)}
sorted_dict = sorted((v,k) for (k,v) in zip(keys, values))
print("The dictionary comprehensions list is as below \n") 
print(dict_comp)
print("The reverse dictionary comprehensions list is as below ") 
print(rev_dict)
print("The sorted dictionary comprehensions list is as below \n") 
print(sorted_dict)
print("\n")
def divide():
    try:
        m=int(input('m is '))
        n=int(input('n is '))
        ans=m//n
        print('Answer is : ', ans)
    except:
        print('Division not possible')
class task:
    #t = task()
    def odd_or_even(num):
        num=int(input('Enter the number: '))
        if(num%2==0):
            print(num,' is an even number')
        else:
            print(num,' is an odd number')
    def pos_or_neg(num):
        num=int(input('Enter the number: '))
        if(num>0):
            print(num,' is a positive number')
        else:
            print(num,' is a negative number')
    def prime_num(num):
        num=int(input('Enter the number: '))
        for i in range(2,num):
            if(num%i==0):
                print(num,' is not a prime number')
                break
            else:
                print(num,' is a prime number')
ta=task()

def main():
    print("*******************")
    print("The main function")
    print("*******************")
    print("\n")
    print("Try and Except")
    print("--------------")
    divide()
    print("\n")
    print("Decision making statements and looping statements")
    print("-------------------------------------------------")
    print("\n")
    print("****************************************")
    print("1. Odd or Even number")
    print("2. Positive or Negative")
    print("3. To check for Prime number")
    print("****************************************")
    print("\n")
    print("Enter your choice: ")
    choice=int(input())
    print("\n")
    if(choice==1):
        print('This  is odd or even function:')
        ta.odd_or_even()
    elif(choice==2):
        print('This is positive or negative function:')
        ta.pos_or_neg()
    elif(choice==3):
        print('This is a prime number function:')
        ta.prime_num()
    elif(choice!=1 or choice!=2 or choice!=3):
        print('Oops! there is no such choice!')
    task()
if __name__ == "__main__":
    main()