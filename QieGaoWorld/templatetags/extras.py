'''
@Author: chiaki
@Date: 2019-10-16 00:24:28
@LastEditors: chiaki
@LastEditTime: 2020-07-04 11:25:25
@Description: 
'''
from django import template

register = template.Library()

@register.filter
def select(value,args):
    multiple=""
    if 'multiple' in value:
        multiple='multiple="multiple"'
        value=value[1:]
    return '<select class="uk-select animal_options" %s >%s</select>' % (multiple,option(value,args))
    
@register.filter
def option(value,args):
    option=""
    _value=""
    _id=None
    for v in value:
        if type(v) == dict:
            _value=v['value']
            _id=v['id']
            if v['id'] == None:
                v['id']=_value
            if v['id'] in args :
                selected="selected"
            else:
                selected=""
        else:
            _value=v.value
            _id=v.id
            if v.id == None:
                v.id=v.value
            if v.id in args :
                selected="selected"
            else:
                selected=""
        
        option +='<option value="%s"%s>%s</option>' % (str(_id),selected,str(_value))
    
    return option

@register.filter
def length(value,args):
    return len(value)

@register.filter
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]
