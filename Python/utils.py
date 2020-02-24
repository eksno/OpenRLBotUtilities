def to_location(target):
	if isinstance(target, Vector3):
  		return target
	elif isinstance(target, list):
  		return Vector3(target)
	elif isinstance(target, tuple):
  		return Vector3(list(target))
	elif isinstance(target, np.ndarray):
  		return Vector3(target.tolist())
	else:
  		return target.location


def rotator_to_matrix(object):
	r = object.rotation.data
	CR = math.cos(r[2])
	SR = math.sin(r[2])
	CP = math.cos(r[0])
	SP = math.sin(r[0])
	CY = math.cos(r[1])
	SY = math.sin(r[1])

	matrix = []
	matrix.append(Vector3([CP*CY, CP*SY, SP]))
	matrix.append(Vector3([CY*SP*SR-CR*SY, SY*SP*SR+CR*CY, -CP * SR]))
	matrix.append(Vector3([-CR*CY*SP-SR*SY, -CR*SY*SP+SR*CY, CP*CR]))
	return matrix
    
def spline(points, locations, distances):
	tck = interpolate.splrep(distances, locations)
	return interpolate.splev(points, tck)
