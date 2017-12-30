def interestingContigs(input, output_file):
        import pandas as pd

        import ast
        df = pd.read_table(input, sep="\t", index_col = 0) #"asmbly_metr.st.bam_info.txt"
        df['interesting'] = False

        for index, row in df.iterrows():

                row['cigtup'] = ast.literal_eval(row['cigtup'])

                SLength = MLength = interruption = interesting = 0
                S = M = False

                for element in row['cigtup']:

                        if(element[0] != 0 | element[0] != 4):
                                interruption = interruption + element[1]
                                if(interruption >= 50): #too long of an interruption
                                        interruption = 0
                                        SLength = MLength = 0

                        if(element[0] == 0): #0 = Match 
                                MLength = MLength + element[1]
                                if(MLength >= 500):
                                        M = True

                        if(element[0] == 4): #4 = Soft clipped
                                SLength = SLength + element[1]
                                if(SLength >= 500):
                                        S = True                 
                        if(S == True & M == True): #need a long soft clipped AND long matched 
                                df.ix[index, 'interesting'] = True
                                break

        dfInteresting = df.query('interesting == True')
        dfInteresting
        dfInteresting.to_csv(output_file)

