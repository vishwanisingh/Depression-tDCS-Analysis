import papermill as pm

# for ACTIVE_SHAM in ['Active', 'Sham']:
#     existing_file = f"comparison-results/result-{ACTIVE_SHAM}.xlsx"
#     df = pd.read_excel(existing_file, header=[0,1])

#     main_column_names = ['index', 'swi', 'links', 'asymmetry', 'regions']
#     subcols = ('delta-g1', 'delta-g2', 'theta-g1', 'theta-g2', 'alpha1-g1', 'alpha1-g2', 'alpha2-g1', 'alpha2-g2', 
#             'beta1-g1', 'beta1-g2', 'beta2-g1', 'beta2-g2', 'beta3-g1', 'beta3-g2', 'gamma-g1', 'gamma-g2')

#     subcolumn_names = {
#         'index' : ['index'],
#         'swi': subcols,
#         'links': subcols,
#         'asymmetry': subcols,
#         'regions': ('delta', 'theta', 'alpha1', 'alpha2', 'beta1', 'beta2', 'beta3', 'gamma')
#     }

#     columns_tuples = [(main_col, sub_col) for main_col in main_column_names for sub_col in subcolumn_names[main_col]]
#     columns = pd.MultiIndex.from_tuples(columns_tuples)
#     df = pd.DataFrame(columns=columns)
#     df.to_excel(existing_file, index=True, header=True)

for ACTIVE_SHAM in ['Active']:
    for ELECTRODES in ['32electrodes', '32electrodes-old']:
        if ELECTRODES == '32electrodes':
            SAMPLES = ['Hemlata', 'Malti', 'Preeti', 'Sharifa', 'Vinita', 'VKS']  if ACTIVE_SHAM == 'Active' else ['Geeta', 'Jitendra', 'Jyoti', 'Kuldeep', 'Seema', 'VijayLaxmi']
        elif ELECTRODES == '32electrodes-old':
            SAMPLES = ['Nitu', 'Ranjeet', 'Resham', 'Rithik', 'Rohan', 'Suman'] 

        notebook_path = 'pre_vs_post.ipynb'

        for SAMPLE in SAMPLES:
            output_notebook_path = f"output_notebook_path/{notebook_path[:-6]}_{SAMPLE}.ipynb"
            pm.execute_notebook(
                input_path=notebook_path,
                output_path=output_notebook_path,
                parameters=dict(SAMPLE=SAMPLE, ACTIVE_SHAM=ACTIVE_SHAM, ELECTRODES=ELECTRODES),
                log_output=True
            )
