# Writing data to a file (overwrites existing content)
with open('example.txt', 'w') as file:
    file.write("Hello, this is an example.\n")
    file.write("Writing multiple lines is easy.\n")
