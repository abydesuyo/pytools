import math
import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

@timer    
def nextPrime(n):
	while True:
		n , isprime = isPrime(n) 
		if isprime:
			return n


def isPrime(n):
	# for i in range(2, round(math.sqrt(n))):
	# i=2
	# while i <  round(math.sqrt(n)): 
	for i in range(2, round(math.sqrt(n))):
		# if i > 2 and i % 2 ==0:
		# 	i+=1
		# if i % 2 == 0:
		# 	i += 1 
		if n%i == 0:
			return n+1, False
		# i += 1
	return n, True

# def nextPrime(n):
# 	while True:
# 		i=2
# 		while i < round(math.sqrt(n)):
# 			if n % i == 0 :
# 				n += 1
# 				break
# 			i += 1 if i % 2 else 2
# 		return n	

n=19876543201143
print(nextPrime(n+1))

