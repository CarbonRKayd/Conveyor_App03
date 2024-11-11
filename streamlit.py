import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import re
import os

from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

dir_list = {}

# Print results.
for row in df.itertuples():
    ###st.write(f"{row.Name} has a :{row.Link}:")
    ###dir_list[row.Index] = row.Name
    dir_list[row.Index] = {"Name": row.Name, "Link": row.Link}

# Create a mapping of Name to Index for the selectbox options
name_to_index = {value["Name"]: index for index, value in dir_list.items()}
    
#category_Output = "C:\\Users\\RamachandranV\\Desktop\\cmd\\2049\\Scene_Category_output_2049_R1.xlsx"

#####category_Output = "C:\\Users\\RamachandranV\\Desktop\\cmd\\2049\\Scene.xlsx"

#path = "C:\\Users\\RamachandranV\\Desktop\\Project\\Python\\Dashboard\\2031\\"
#dir_list = os.listdir(path)
##st.write(dir_list)

st.write("# Welcome to Carbon RKayd!")

st.markdown(
            """
                    

                    ### Choose a Asset Input File
            """

                
                )


#####Intput_File_new = st.file_uploader(" ")

selected_name = st.selectbox(
         'Please Select the Project Asset File from below Option',
         ###list(dir_list.values()),
         options=list(name_to_index.keys()),  # Display Names as options
         index=None,
         placeholder="Select the Asset File...",
        )
# Retrieve the corresponding link for the selected name
selected_index = name_to_index[selected_name]
st.write(selected_name)
st.write(selected_index)
Input_File_new = dir_list[selected_index]["Link"]
st.write(Input_File_new)
#st.write('You selected:', Intput_File_new)

st.markdown(
        """
        **👈 Select a Conveyor from the dropdown on the left**     
    """
    )

##category_Output = "C:\\Users\\RamachandranV\\Desktop\\Project\\Python\\Dashboard\\2031\\Assert.xlsx"

#Dir = "C:\\Users\\RamachandranV\\Desktop\\Project\\Python\\Dashboard\\2031\\"

#category_Output = os.path.join(Dir, Intput_File_new)

if Intput_File_new is not None:

    #category_Output = os.path.join(Dir, Intput_File_new)

    categories = {
        'Conveyor': ['_'],
        'Photo device': ['PE'],
        'Push Button': ['PB'],
        'Proximity': ['PX'],
        'Control Relay': ['CR'],
        'Emergency Stop': ['ES','ER'],
        'Global Light': ['GL'],
        'Logic_Motor': ['MA'],
        'Scanner': ['MS'],
        'Motor': ['M'],
        'Control Cab': ['CC'],
        'Encoder': ['EN'],
            
    }

    def categorize(text):
        if not isinstance(text, str) or len(text) == 0:
            return 'Uncategorized'  # Handle empty or non-string cases
        
        first_letter = text[0].upper()  # Get the first letter and convert to uppercase
        first_two_letters = text[:2].upper()  # Get the first two letters and convert to uppercase
        
        for category, patterns in categories.items():
            if first_letter in patterns or first_two_letters in patterns:
                return category
        return 'Uncategorized'  # Default if no patterns match



    #df = pd.DataFrame(data)

    con1 = st.connection("gsheets", type=GSheetsConnection)

    #####df = con1.read(spreadsheet="https://docs.google.com/spreadsheets/d/1F6El9swNECMEvH6mFx16PkAfVbe8_7UTwQrRLhCRttY/edit?gid=1438290628#gid=1438290628",worksheet="EquipmentProperty")

    df = con1.read(spreadsheet=Intput_File_new,worksheet="EquipmentProperty")


    #####df = pd.read_excel(Intput_File_new, sheet_name='EquipmentProperty')

    # Split the 'Path' column
    df[['Conveyor', 'Device']] = df['{LocationPath}'].str.split('\\', expand=True).iloc[:, -2:]

    # Perform the split only on non-null values
    #df[['Conveyor', 'Device']] = df['{LocationPath}'].apply(
    #    lambda x: x.split('\\')[-2:] if isinstance(x, str) else [None, None]
    #).apply(pd.Series)

    # Rename columns for clarity
    #df = df.rename(columns={'Column1': 'Conveyor', 'Column2': 'Device'})

    df['Category'] = df['Device'].apply(categorize)

    df['Conveyor'] = df['Conveyor'].fillna('') 

    ##--------------------st.markdown("Input_Data")

    ##--------------------st.dataframe(df)

    dynamic_filters = DynamicFilters(df, filters=['Conveyor'])

    st.markdown("""
    <style>
        [data-testid=stSidebar] {
          background-color: #262B41;
         }
   </style>
   """, unsafe_allow_html=True)


    with st.sidebar:
        st.markdown('''
          :gray[Select Conveyor from below] ''')

    dynamic_filters.display_filters(location='sidebar')

    ##--------------------st.markdown("Filtered Data")

    ##--------------------dynamic_filters.display_df()

    
       

    filtered_df = dynamic_filters.filter_df()


    filtered_df1 = filtered_df.drop(['{LocationPath}','DisplayName','Description','SortOrder','Guid','ItemOrigin','Enabled','UnitOfMeasureID','RangeMinimum','RangeMaximum','TimeZoneType','TimeZone','SelectedProducts','RuntimeParameters','RealtimePointType','RealtimeDataType','RealtimeReadExpression','RealtimeWriteExpressionEnabled','RealtimeWriteExpression','RealtimeAlwaysOnScan','RealtimeScanRate','RealtimeQualityFilter','UseDatabaseCache','PollingGroupID','HistoryPointType','HistoryPointDifferent','HistoryPointName','DatasetType','DatasetPointName','EventsType'], axis=1, inplace=True)

    #filtered_df1 = filtered_df1[['Conveyor','Device','Category','Name','RealtimePointName','RealtimeValue','Description']]

    #final_PE = filtered_df[filtered_df['Category'].isin(['Photo device'])]

    #st.dataframe(final_PE)

    final_Motor = filtered_df[filtered_df['Category'].isin(['Motor'])]

    

    ######st.dataframe(final_Motor)

    # Extract "PE" codes including suffix and save as list
    #pe_codes = final_Motor['RealtimePointName'].str.extractall(r"(PE\d+_\w+)")[0].tolist()

    #st.dataframe(pe_codes)


    # Define a function to extract input and target parts
    def extract_parts(row):
        # Check if the row contains a string
        if isinstance(row, str):
            # Check if the row contains '||'

            # Check if the data contains 'ac:Lipman Brothers Nashville/Set_False'
            if 'ac:Lipman Brothers Nashville/Set_False' in row:
                return pd.Series([None, None], index=['input', 'extracted'])

            if '||' in row:
                # Split by '||' if present
                parts = row.split("||")
                inputs = []
                extracted_parts = []
                
                # Process each part
                for part in parts:
                    # Extract input part (everything after '{{' until '}}')
                    input_part = re.search(r'\{\{(.+?)\}\}', part)
                    if input_part:
                        inputs.append(input_part.group(1))
                    
                    # Extract part between the second and third slashes
                    extracted_part = re.search(r'/([^/]+)/[^/]+}}', part)
                    if extracted_part:
                        extracted_parts.append(extracted_part.group(1))
                
                return pd.Series([inputs, extracted_parts], index=['input', 'extracted'])
            
            else:
                # Handle the case where '||' is not present
                parts = row.split('/')
                inputs = []
                extracted_parts = []
                
                # Extract the part between the second and third slash (i.e., the PE code)
                if len(parts) >= 4:
                    extracted_part = parts[2]  # This is the part between the second and third slash
                    extracted_parts.append(extracted_part)
                
                return pd.Series([inputs, extracted_parts], index=['input', 'extracted'])
        
        else:
            # Return None for rows that aren't strings
            return pd.Series([None, None], index=['input', 'extracted'])



    # Apply the function to each row in the DataFrame
    final_Motor[['input', 'extracted']] = final_Motor['RealtimePointName'].apply(extract_parts)

    # Create a placeholder for the DataFrame or message
    placeholder = st.empty()

    # Checkbox to show or hide the DataFrame
    show_dataframe = st.checkbox("View Conveyor Configuration")

    if show_dataframe:
        placeholder.dataframe(final_Motor)

    #print(df[['input', 'extracted']])

    ###-----------------st.dataframe(final_Motor)

    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Run Status']
    Status_value = selected_row['RealtimePointName'].values[0]  # Extracting the value from column 'A'

    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Fault Status']
    Fault_value = selected_row['RealtimePointName'].values[0]  # Extracting the value from column 'A'

    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Name']
    Motor_Name = selected_row['RealtimeValue'].values[0]  # Extracting the value from column 'A'

    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Name']
    Conveyor_Name = selected_row['Conveyor'].values[0]  # Extracting the value from column 'A'


    Motor_list =[]
    Motor_list =[("Conveyor",Conveyor_Name),("Motor",Motor_Name),("Run_Status",Status_value),("Fault_Status",Fault_value)]
    df_data = pd.DataFrame(Motor_list, columns=["Name", "Value"])
    ####------------st.markdown("Motor")
    ####------------st.dataframe(df_data)



    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Jam Status']
    # If you want to select specific values from other columns, such as column 'A
    value_from_column = selected_row['extracted'].values[0]  # Extracting the value from column 'A'
    ####st.write(value_from_column)
    ####st.dataframe(filtered_df)
    # Update the list with the names of the IDs that exist in the DataFrame
    #updated_list = [filtered_df.loc[filtered_df['Device'] == i, 'RealtimePointName'].values[0] if i in filtered_df['Device'].values else None for i in value_from_column]
    target = 'Jam Status' 
    ####------------st.markdown("Photot device")
    # Ensure 'value_from_column' is iterable (not None)
    if value_from_column is not None and hasattr(value_from_column, '__iter__'):
        updated_list_PE = [
            (i, df.loc[(df['Device'] == i) & (df['Name'] == target), 'RealtimePointName'].values[0]) 
            for i in value_from_column
            if not df.loc[(df['Device'] == i) & (df['Name'] == target)].empty
        ]
    else:
        updated_list_PE = []  # Or handle it differently if needed
    # Display the updated list
    ####------------st.dataframe(updated_list_PE)  # Output will be 2



    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Emergency Stop']
    # If you want to select specific values from other columns, such as column 'A'
    value_from_column = selected_row['extracted'].values[0]  # Extracting the value from column 'A'
    ####------------st.markdown("Emergency Stop")
    target = 'Status' 
    # Update the list with the names of the IDs that exist in the DataFrame and match the condition (Age)
    if value_from_column is not None and hasattr(value_from_column, '__iter__'):
        updated_list_ES = [
            (i,df.loc[(df['Device'] == i) & (df['Name'] == target), 'RealtimePointName'].values[0]) 
            #if i in filtered_df['Device'].values and (filtered_df['Name'] == target) 
            for i in value_from_column
            if not df.loc[(df['Device'] == i) & (df['Name'] == target)].empty 
                    
        ]
    else:
        updated_list_ES = []
    ####------------st.dataframe(updated_list_ES)  # Output will be 2




    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Full Line']
    # If you want to select specific values from other columns, such as column 'A'
    value_from_column = selected_row['extracted'].values[0]  # Extracting the value from column 'A'
    ####------------st.markdown("Full Line")
    target = 'Full Line' 
    # Update the list with the names of the IDs that exist in the DataFrame and match the condition (Age)
    if value_from_column is not None and hasattr(value_from_column, '__iter__'):
        updated_list_Full = [
            (i,df.loc[(df['Device'] == i) & (df['Name'] == target), 'RealtimePointName'].values[0]) 
            #if i in filtered_df['Device'].values and (filtered_df['Name'] == target) 
            for i in value_from_column
            if not df.loc[(df['Device'] == i) & (df['Name'] == target)].empty 
                    
        ]
    else:
        updated_list_Full = []
    ####------------st.dataframe(updated_list_Full)  # Output will be 2



    # Let's say we want to select the row where column 'B' has the value 'banana'
    selected_row = final_Motor[final_Motor['Name'] == 'Half Line']
    # If you want to select specific values from other columns, such as column 'A'
    value_from_column = selected_row['extracted'].values[0]  # Extracting the value from column 'A'
    ####------------st.markdown("Half Line")
    target = 'Half Line' 
    # Update the list with the names of the IDs that exist in the DataFrame and match the condition (Age)
    if value_from_column is not None and hasattr(value_from_column, '__iter__'):
        updated_list_Half = [
            (i,df.loc[(df['Device'] == i) & (df['Name'] == target), 'RealtimePointName'].values[0]) 
            #if i in filtered_df['Device'].values and (filtered_df['Name'] == target) 
            for i in value_from_column
            if not df.loc[(df['Device'] == i) & (df['Name'] == target)].empty 
                    
        ]
    else:
        updated_list_Half = []
    ####------------st.dataframe(updated_list_Half)  # Output will be 2

    #col1, col2, col3 = st.columns(3)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Motor", "Photo Device", "E-Stop", "Full Line", "Half Line"])

    with tab1:            
      st.subheader("Motor")
      st.dataframe(df_data)
    with tab2:
      st.subheader("Photot device")
      st.dataframe(updated_list_PE)
    with tab3:
      st.subheader("Emergency Stop")
      st.dataframe(updated_list_ES)
    with tab4:
      st.subheader("Full Line")
      st.dataframe(updated_list_Full)
    with tab5:
      st.subheader("Half Line")
      st.dataframe(updated_list_Half)



