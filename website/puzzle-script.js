// SpydirWebz Puzzle JavaScript - Murdle Inspired
document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('check-solution');
    const resultDiv = document.getElementById('solution-result');
    const gridCells = document.querySelectorAll('.grid-cell');
    
    if (checkButton && resultDiv) {
        checkButton.addEventListener('click', checkSolution);
    }
    
    // Interactive Logic Grid
    gridCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const currentState = this.className;
            
            // Cycle through states: empty -> marked -> eliminated -> empty
            if (currentState.includes('marked')) {
                this.className = 'grid-cell eliminated';
            } else if (currentState.includes('eliminated')) {
                this.className = 'grid-cell';
            } else {
                this.className = 'grid-cell marked';
            }
        });
        
        // Right click to eliminate
        cell.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            if (!this.className.includes('marked')) {
                this.className = 'grid-cell eliminated';
            }
        });
    });
    
    function checkSolution() {
        const actor = document.getElementById('solution-actor').value;
        const vector = document.getElementById('solution-vector').value;
        const asset = document.getElementById('solution-asset').value;
        const data = document.getElementById('solution-data').value;
        
        if (!actor || !vector || !asset || !data) {
            showResult('Please select all solution components.', 'incorrect');
            return;
        }
        
        // Get the correct solution from embedded puzzle data
        const solution = puzzleData.solution;
        const isCorrect = 
            actor === solution.actor &&
            vector === solution.vector &&
            asset === solution.asset &&
            data === solution.stolen_data;
        
        if (isCorrect) {
            showResult('🎉 Correct! You solved the puzzle!', 'correct');
        } else {
            const correctAnswer = `${solution.actor} used ${solution.vector} against ${solution.asset} to steal ${solution.stolen_data}`;
            showResult(`❌ Incorrect. The correct answer is: ${correctAnswer}`, 'incorrect');
        }
    }
    
    function showResult(message, type) {
        resultDiv.textContent = message;
        resultDiv.className = `solution-result ${type}`;
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && checkButton) {
            checkSolution();
        }
    });
});