def round_tuple(value):
	return tuple([int(i) for i in value])

def clamp(val, min, max):
	return ((val if min < val else min) if max > val else max)
