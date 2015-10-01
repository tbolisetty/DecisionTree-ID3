class Node(object):
	def __init__(self,attribute_name,attribute_value_map,used_attribute_list,total_attribute_list):
		self.attribute_name=attribute_name
		# ---stores the map of each attribute_name and its associated class map
		self.attribute_value_map=attribute_value_map
		# ---stores all child nodes with perticular attribute_value as {attribute_value,Node}
		self.children=dict();
		# ---contains {attribute_name,attribute_value} which have been used
		self.used_attribute_value_map=dict();
		# ---stores all used attributes list
		self.used_attribute_list=used_attribute_list
		# ---stores total number of attributes 
		self.total_attribute_list=total_attribute_list
		# ---contains class value for particular attribute_value
		self.class_value=dict();
		
	def add_child(self,attribute_name,obj):
		self.children[attribute_name]=obj;
	
	def add_attribute_in_list(self,att):
		self.used_attribute_list.append(att)
	
	def add_attribute_value_map(self,attribute_value):
		self.used_attribute_value_map[attribute_name]=attribute_value
	
	def set_attribute_value_map(self,used_attribute_value_map):
		self.used_attribute_value_map=used_attribute_value_map
		
	def get_attribute_value_map(self):
		return self.used_attribute_value_map;
		
	def set_class_value(self,att_value,class_value):
		self.class_value[att_value]=class_value;
		
	def get_used_attribute_list(self):
		return self.used_attribute_list;

		

class AttValues(object):
		map=dict();
		total_count=0;
		
		def __init__(self,map,total_count):
			self.map=map
			self.total_count=total_count


class AttributeNameMap(object):
	map=dict()
	name='';
	def __init__(self,name,map):
		self.name=name;
		self.map=map
		