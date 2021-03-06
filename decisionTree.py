import csv
import math
import tree 
import sys
import copy
class_value_set=set();
global feature_vector_length
featureVectorList=[]
# global round
def read(train_data_set):
	# round=0
# ----create list of hashmaps for storing training row data
	with open(train_data_set) as mush_train:
		reader=csv.reader(mush_train)
		for row in reader:
			featureVectorMap=dict();
			for x in range(0,len(row)):
				key='Att_'+str(x);
				featureVectorMap[key]=row[x];
				if x==0:
					class_value_set.add(row[x])
			featureVectorList.append(featureVectorMap);
	global feature_vector_length
	feature_vector_length=len(featureVectorList[0]);
	# print('length' ,feature_vector_length)
	
	
def decision_tree():
	# ---get the best attribute and list of all attributes
	best_attribute,att_class_map=find_best_attribute(featureVectorList,{});
	# ---create parent node with attribute name, attribute class map, used attribute list,total attribute list
	# ---if children map is empty and class map is empty then create tree
	best_attribute_name='Att_'+str(best_attribute)
	global feature_vector_length
	# print('global ',feature_vector_length)
	parent=tree.Node(best_attribute_name,att_class_map,[best_attribute_name],feature_vector_length);
	construct_tree([parent]);
	return parent
	
	
def construct_tree(node_list):
	# print(node_list)
	if not node_list:
		return;
	bfs_list=[];
	for node in node_list:
		# --- calculate the entropy of the node.
		for attribute_value,attribute_class_map in node.attribute_value_map.items():
			entropy=calculate_class_entropy(attribute_class_map.map);
		# ---check if the entropy of node is zero or if all the attributes are utilised
			class_value=0;
			# print(len(node.used_attribute_list),(node.total_attribute_list-1))
			if (len(node.used_attribute_list)-(node.total_attribute_list-1))==0 or (entropy==0):
				class_value_list=list(class_value_set);
				for k,v in attribute_class_map.map.items():
					class_value=k	
				if (entropy!=0):
					class_count=-1;
					# print(node.attribute_name, attribute_class_map.map.items())
					for k,v in attribute_class_map.map.items():
						# print(v)
						if class_count<v:
							class_value=k;
							class_count=v
				# print('class value ',class_value)		
				node.set_class_value(attribute_value,class_value)
				continue;
		# -----if not calculate the next best attribute to divide
			else:
				used_attribute_value_map=node.get_attribute_value_map()
				used_attribute_value_map[node.attribute_name]=attribute_value;
				new_featureVectorList=[]
				# ---get all featurevectors for which are not used after matching with the used_attribute_list 
				for featureVectorMap in featureVectorList:		
					matched_attributes=set(featureVectorMap.items())&set(node.used_attribute_value_map.items())
					if (matched_attributes==set(node.used_attribute_value_map.items())) :
						new_featureVectorList.append(featureVectorMap)
				if not new_featureVectorList:
					return
				# --- find best attribute from new featureVectorList
				# print(node.attribute_name,node.used_attribute_list)
				best_attribute,att_class_map=find_best_attribute(new_featureVectorList,node.used_attribute_list);
				# ----create nodes for the subtype of this best attribute 
				child=create_node(node,best_attribute,att_class_map);
				node.add_child(attribute_value,child);
				# --- append all the children to the bfs_list for complete tree
				bfs_list.append(child);
				# print('child att', child.attribute_name)
		# ---add for unknown attribute 
		# -----
	# --- call the construct_tree for the new bfs_list again 
	# print('list is', bfs_list)
	construct_tree(bfs_list)
	# ----add the best attribute in the nodes used_attribute_list 
	
	# ----add these nodes in the bfs_list for calling recursively
		
def create_node(parent,best_attribute,att_class_map):
	best_attribute_name='Att_'+str(best_attribute)
	used_attribute_list=copy.deepcopy(parent.get_used_attribute_list());
	used_attribute_list.append(best_attribute_name);
	used_attribute_value_map=copy.deepcopy(parent.get_attribute_value_map());
	
	child=tree.Node(best_attribute_name,att_class_map,used_attribute_list,feature_vector_length)
	child.set_attribute_value_map(used_attribute_value_map)
	return child
	
def find_best_attribute(featureVectorList,considered_attributes):
#---creating a list of attribute size with {attribute_value:{class_value:count}}
	# print(featureVectorList)
	att_list=[{} for _ in range(len(featureVectorList[0])-1)];
	for featureVectorMap in featureVectorList:
		for x in range(1,len(featureVectorMap)):
			att='Att_'+str(x);
			if att in considered_attributes:
				continue;
			else:
				count=1;
				att_value=featureVectorMap['Att_'+str(x)];
				class_value=featureVectorMap['Att_'+str(class_index)];
				#---if attribute value is present in attribute list then find the class value and increment it
				if  att_value in att_list[x-1]:
					att_map_object=att_list[x-1][att_value];
					if class_value in att_map_object.map:
						count=att_map_object.map[class_value]+1;
					att_map_object.map[class_value]=count;
					att_map_object.total_count=att_map_object.total_count+1;
				else:
					map=dict();
					map[class_value]=count;
					att_map_object=tree.AttValues(map,1);
					att_list[x-1][att_value]=att_map_object
					# att_list[x-1][att_value]=map;
	i=1;
	max_information_gain=-1;
	attribute_information_node=0;
	decision_map=dict();
	att_information_gain=0;
	class_hashmap=get_class_hashmap(featureVectorList);
	class_entropy=calculate_class_entropy(class_hashmap);
	
	for att in att_list:
		name='Att_'+str(i)
		if not att.items(): #or name in considered_attributes:
			i+=1;
			continue;
		else:
			att_information_gain=class_entropy - calculate_att_entropy(att);
			# print(name,att_information_gain)
			if max_information_gain < att_information_gain:
				max_information_gain=att_information_gain;
				attribute_information_node=i;
			i+=1;
			global round
	# print('-------------------', round, '-------------------')	
	# print('max att information ',attribute_information_node , max_information_gain )
	# ---send best attribute number with its class map 
	round=round+1;
	return attribute_information_node,att_list[attribute_information_node-1]

def calculate_att_entropy(att_map):
	att_entropy=0;
	sample_space=0;
	for att_value,att_value_obj in att_map.items():
		sample_space=sample_space+att_value_obj.total_count;
	for att_value,att_value_obj in att_map.items():
		att_value_map=att_value_obj.map;
		total_count=att_value_obj.total_count;
		e=0;
		for class_value,count in att_value_map.items():
			e=e+calculate_entropy(count,total_count);
		att_entropy=att_entropy+(total_count/sample_space)*e;
		# print(att_value,att_entropy)
	return att_entropy;
	
def calculate_entropy(val,sample_space):
	p=val/sample_space;
	entropy=-(p*math.log(p,2));
	return entropy;
	
def get_class_hashmap(featureVectorList):
	sample_space=0;
	entropy=0;
	hash_class=dict();
	
	for map in featureVectorList:
		x=map['Att_'+str(class_index)];
		# print(x)
		count=1;
		if(x in hash_class):
			count=hash_class[x]+1;
			# count=count+1;
		hash_class[x]=count;
	# print(hash_class)
	return hash_class
	
	
def calculate_class_entropy(hash_class):
	class_entropy=0;
	class_total=0;
	for key,val in hash_class.items():
		class_total=class_total+val;
	
	for key,val in hash_class.items():
		class_entropy+=calculate_entropy(val,class_total);
	
	return class_entropy;
	
	
def print_tree(root,att_details,space):
	attribute=att_details[root.attribute_name]
	print(attribute.name)
	
	x=len(attribute.name)+space
	if root.class_value:
		for k,v in root.class_value.items():
			for i in range(1,x):
				print(' ',end="")
			print(': '+ attribute.map[k]+ ' : '+v,);	
	
	if root.children:
		for k,v in root.children.items():
			for i in range(1,x):
				print(' ',end="")
			print(': '+ attribute.map[k] +' : ',end="" )
			space=space+len(attribute.name)+ len(attribute.map[k])+5;
			print_tree(v,att_details,space);


	
def parseTrainData(root,test_data_set):
	parse_featureVectorList=[]
	output=open('/output.data','w')
	with open(test_data_set) as mush_train:
		reader=csv.reader(mush_train)
		for row in reader:
			parse_featureVectorMap=dict();
			for x in range(0,len(row)):
				key='Att_'+str(x);
				parse_featureVectorMap[key]=row[x];
			parse_featureVectorList.append(parse_featureVectorMap);
	i=1
	hits=0
	for parse_featureVectorMap in parse_featureVectorList:
		parent=root;
		val=parse_featureVectorMap[parent.attribute_name]
		# ---check val is present in parents attribute list
		while True:
			if val in parent.attribute_value_map:
				# -- check if val is in class_value ie it has direct leaf 
				if val in parent.class_value:
					out_value=parent.class_value[val];
					break;
				else:
					parent=parent.children[val]
					val = parse_featureVectorMap[parent.attribute_name]
			# ---attribute value not present in node
			else:
				# ---find maximum probability child value and assign
				new_class_map=dict();
				
				for att_value,class_map in parent.attribute_value_map.items():
					# if att_value in parent.class_value:
						for class_v,class_value_count in class_map.map.items():
							if class_v in new_class_map:
								new_class_map[class_v]=class_value_count+new_class_map[class_v];
							else:
								new_class_map[class_v]=class_value_count;
				count=0;
				out_value=0;
				for k,v in new_class_map.items():
					if v>count:
						out_value=k
						count=v
				break;
		flag='False'
		if(out_value==parse_featureVectorMap['Att_'+str(class_index)]):
			hits+=1;
			flag='True';
		
		output.write(str(out_value) + "," +flag + '\n');
		i+=1;
	
	accuracy=hits/len(parse_featureVectorList)
	print(accuracy*100)
	output.close()
	mush_train.close()
	
def attribute_mapping(attribute_mapping_file):
	att_details=dict();		
	file=open(attribute_mapping_file)
	x='Att_'
	i=1;
	for line in file:
		att_value_map=dict();
		att=line.split(": ")
		name=att[0].split('. ')[1]
		map={v.rstrip():k for k,v in (x.split('=') for x in att[1].split(','))}
		attribute_obj=tree.AttributeNameMap(name,map)
		att_details['Att_'+str(i)]=attribute_obj
		i+=1;
	return att_details
global round 
round = 0
def main(args):
	train_data_set= args[1]
	test_data_set=args[2]
	attribute_mapping_file=args[3]
	global class_index 
	
	#round=0;
	class_index =0
	read(train_data_set);
	# for x in featureVectorList:
		# print(x['Att_0'])
	parent=decision_tree();
	att=attribute_mapping(attribute_mapping_file);
	print_tree(parent,att,1);
	print('Accuracy of decision tree on training set : ',end="")
	parseTrainData(parent,train_data_set);
	print('Accuracy of decision tree on test set : ',end="")
	parseTrainData(parent,test_data_set);
	
main(sys.argv)





