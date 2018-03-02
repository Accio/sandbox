Concatenate every two lines in a text file with tab ('\t')
```{bash}
echo -e 'Line1\nLine2\nLine3\nLine4' | sed '$!N;s/\n/\t/'
```
A good explanation why this works can be found [here by terdon on StackOverflow](https://askubuntu.com/questions/461191/what-is-the-meaning-of-an-in-a-sed-command)
