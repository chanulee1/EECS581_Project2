## 09/16/2024

**Time spent on project:** 30 minutes

**Brief summary of what you did:** I downloaded and installed all of the dependencies the project required. I also went through and familiarized myself with their structure, format, and overall organization.



## 09/19/2024

**Time spent on project:** 4 hours

**Brief summary of what you did:** Made a new section on the pygame main menu for difficulty. You can select either easy, medium, hard, or pvp. Also added new difficulty var to the necessary files.



## 09/23/2024

**Time spent on project:** 9 hours

**Brief summary of what you did:** Set up the AI and has it place ships randomly. Also got turns working for AI difficulties. Set up barebones AI difficulty functions so that each difficulty can have its area of thinking. Time for this day is an aggregation of the weekends time because I didn't finish my thoughts until today. Handled duplicate attacks for if the difficulty is easy. Updated the win message if the AI wins. Implemented Easy Difficulty



## 09/26/2024

**Time spent on project:** 1 hour

**Brief summary of what you did:** Fixed a bug where the AI would retain its previously placed pieces if an error was found in its placement. This meant that when it started placing the ships again, there would already be ships on the grid making it more likely for another error. This would eventually lead to an infinite loop of trying to place pieces and then it throwing an exception. We now clear the board before it attempts its placement of its pieces now.