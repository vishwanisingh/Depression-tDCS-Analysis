Mention file_path from any ipynb file

Then use common file, it is a global file which has all:
1. Global variables
2. Package imports
3. Data transformation functions, this is specific to EASY Data
4. All plots
5. Other common functions to be used

Preprocessing file has all functions related to preprocessing:
1. Band pass filtering
2. Rereferencing
3. Wavelet denoising
4. Cropping signal
5. Resampling
6. Dropping channels (provided another data is sent)
7. Collective MDD preprocessing
8. Collective control preprocessing

Two comparisons:
1. Individual comparison - Run run_all : pre vs post (active+sham) - with ttest_rel(g1, g2), pre vs control - with ttest_ind(g1, g2)
2. Average comparison - 



# stats
        Distribution    paired 
Active 

Sham 


Normal distribution : parametric testing - t-test / ANOVA
                    non parametric testing - Mann-Whitney U test / WIlocoxon signed rank test
paired : paired t-tests / wilcoxon signed rank test
        non paired - independent t-tests / Mann-Whitney U test
Multiple comaprisons : Bonferroni correction 