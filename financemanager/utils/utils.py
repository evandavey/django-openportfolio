
def full_name(obj):
	""" Returns a parent/child representation of this object
		eg: parent::child1::child_of_child1
	"""
	p_list=[] #empty list to store parent names
	parent=None
	while True:	
		try:
			if parent is None: #first time through loop
				parent=obj.parent
			else:
				parent=parent.parent
			
			#No parent, stop looping.  ObjectDoesNotExist doesn't seem to trigger on new save()
			if parent is None:  
				break
		
			p_list.append(parent.name)
		except ObjectDoesNotExist: 	#No parent, stop looping
			break
		
	p_list.reverse()	
	p_list.append(obj.name)
	
	return "::".join(p_list)