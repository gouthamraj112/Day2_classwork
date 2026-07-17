let marks = [85, 42, 78, 90, 38, 76, 55, 29, 84, 49];
let passed = 0;
let failed = 0;
let max = 0;
let min=marks[0];


for (let i = 0; i < marks.length; i++) {
    if (marks[i] >= 50) {
        console.log("Student " + (i + 1) + ": " + marks[i] + " - Pass");
        passed++;
    } else {
        console.log("Student " + (i + 1) + ": " + marks[i] + " - Fail");
        failed++;
    }
    if(max<marks[i]){
        max=marks[i];
    }
    if(min>marks[i])
    {
        min=marks[i];
    }
}

console.log("Total Passed: " + passed);
console.log("Total Failed: " + failed);
console.log("Highest Marks: " + max);
console.log("Least Marks:"+min )
