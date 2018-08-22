import glass

print(glass.State.Stopped)
glass.State.__stopped = 1
print(glass.State.__stopped)
print(glass.State.Stopped)