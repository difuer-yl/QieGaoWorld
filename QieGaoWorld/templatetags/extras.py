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
