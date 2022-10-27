# Writeup Notes

People seemed to find this one really hard for some reason? There's a structure where you can store data, and the goal is to store an integer 13371337 without being able to directly set that value. In this case, you just input the integer as a raw bytes into the string field, and you bypass the check in the code.