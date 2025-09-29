document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const commentLimitSelect = document.getElementById('comment-limit');
    const resultsDiv = document.getElementById('results');

    analyzeBtn.addEventListener('click', async () => {
        const url = youtubeUrlInput.value;
        const limit = commentLimitSelect.value;

        if (!url) {
            resultsDiv.innerHTML = '<p class="error">Please enter a YouTube URL.</p>';
            return;
        }

        resultsDiv.innerHTML = '<p class="loading">Analyzing... Please wait.</p>';

        try {
            const response = await fetch('http://localhost:8000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url, comment_limit: parseInt(limit) }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An unknown error occurred.');
            }

            displayResults(data);

        } catch (error) {
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    });

    function displayResults(data) {
        // Basic result display - will be improved later
        resultsDiv.innerHTML = `
            <h2>${data.title}</h2>
            <p><strong>Video Summary:</strong> ${data.video_summary}</p>
            <div>
                <h3>Stance Distribution</h3>
                <p>Agreement: ${data.stance_distribution.AGREEMENT.toFixed(2)}%</p>
                <p>Disagreement: ${data.stance_distribution.DISAGREEMENT.toFixed(2)}%</p>
                <p>Neutral: ${data.stance_distribution.NEUTRAL.toFixed(2)}%</p>
            </div>
        `;
    }
});
