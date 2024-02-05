##SurveySamplingFunctions.py

def value_mapping (pdata, variable_name, map_dict, new_variable = None):
    """Given a pandas dataframe, a variable name, and a desired replacement dictionary, change how the variables values are recorded.
    Can also create a new variable instead of replacing by setting a value for new_variable."""
    temp_value = [map_dict.get(value, value) for value in pdata[variable_name]]
    if new_variable:
        pdata[new_variable] = temp_value
    else:
        pdata[variable_name] = temp_value
    return pdata