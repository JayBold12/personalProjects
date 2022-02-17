from typing import List
import random
from timeit import default_timer as timer
def genreateRandomNumbers(amountOfNumbers: int) -> List:
    nums = []
    for i in range(amountOfNumbers):
        num = random.randint(0, amountOfNumbers)
        nums.append(num)
    nums.sort()
    return nums
def linearSearch(nums: List, target: int) -> int:
    start = timer()
    for num in nums:
        if num == target:
            break
    end = timer()
    return end - start
def binarySearch(nums: List, target: int) -> int:
    start = timer()
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l+r) // 2
        if nums[mid] == target:
            break
        if nums[mid] > target:
            r = mid - 1
        if nums[mid] < target:
            l = mid + 1
    end = timer()
    return end - start
def compareTime(l : int, b : int) -> str: 
    if l < b:
        print("Linear Search was able to find your target in " + str(l) + " seconds")
    if l > b:
        print("Binary Search was able to find your target in " + str(b) + " seconds")
    if l == b:
        print("Both searches your target in " + str(l) + " seconds")    
def main():
    #generate list of random numbers
    numbers = genreateRandomNumbers(1000)
    #set target number to find
    target = int(input("Select a number to find: "))
    #time it takes to find the target number via linear search
    linearTime = linearSearch(numbers, target)
    #time it takes to find the target number via binary search
    bianryTime = binarySearch(numbers, target)
    #compare times to each other
    winner = compareTime(linearTime, bianryTime)
if __name__ == "__main__":
    main()