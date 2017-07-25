#! usr/bin/python

print ("hello")

yourAge = int(raw_input("How old are you: "))

if (yourAge > 0) and (yourAge < 120):

    if (yourAge == 35):
        print 'Same as me'

    elif(yourAge > 35):
        print "Older than me"

    else:
        print "Different from me"

else:
    print "Dont lie about your age"
