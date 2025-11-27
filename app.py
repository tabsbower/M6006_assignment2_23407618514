#import libraries
from shiny import App, render, ui, reactive 
import matplotlib.pyplot as plt
import pandas as pd 

#read data
attendance_df = pd.read_csv('attendance_anonymised-1.csv')

#drop planned end date column
attendance_df_new = attendance_df.drop("Planned End Date", axis=1)

# rename the columns
attendance_df_new.rename(columns={"Unit Instance Code": "Module Code", 
                                  "Calocc Code": "Year", 
                                  "Long Description": "Module Name", 
                                  "Register Event ID": "Event ID",
                                  "Register Event Slot ID": "Event Slot ID",
                                  "Planned Start Date": "Date",
                                  "is Positive": "Has Attended",
                                  "Postive Marks": "Attended",
                                  "Negative Marks": "NotAttended",
                                  "Usage Code": "Attendance Code"}, 
                                  inplace=True)

#convert 'Date' column to datetime format
attendance_df_new['Date'] = pd.to_datetime(attendance_df_new['Date'])

#get list of unique modules for dropdown
module_list = sorted(attendance_df_new['Module Name'].unique())

#define UI
app_ui = ui.page_fluid(
    # Add title panel
    ui.panel_title("Student Attendance Dashboard"),
    
    # Add sidebar layout with dropdown
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "module",
                "Select Module:",
                choices=module_list,
                selected=module_list[0]
            )
        ),
        ui.output_plot("attendance_plot")
    )
)

#define server
def server(input, output, session):
    @render.plot
    def attendance_plot():
        # Get selected module from dropdown
        selected_module = input.module()
        
        # Filter dataframe for selected module
        module_df = attendance_df_new[attendance_df_new['Module Name'] == selected_module]
        
        # Group by date and calculate attendance rate
        attendance_rate = module_df.groupby('Date')['Attended'].mean()
        
        # Create plot
        plt.figure(figsize=(10, 4))
        plt.plot(attendance_rate.index, attendance_rate.values, marker='o')
        plt.title(f'Attendance Rate Over Time for {selected_module}')
        plt.xlabel('Date')
        plt.ylabel('Average Attendance Rate')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.gcf()
    
#create app
app = App(app_ui, server)