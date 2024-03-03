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

def system_var (main, sample, sample_key, Is_Sqrt = False):
    """"Calculates the system variance by manually calculating the information for design variance based on population sizes, given two pandas dataframes of the original information and the sample. Population variance calculated through Pandas var."""
    sqr = 0.5 if Is_Sqrt else 1
    s_var = ((len(main)**2)*(1-len(sample)/len(main))*(1/len(sample))*sample[sample_key].var(ddof=0))**sqr
    return s_var
