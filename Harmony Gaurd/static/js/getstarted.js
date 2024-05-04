document.addEventListener('DOMContentLoaded', function () {
    var recordingTimer;
    loadingIcon.classList.add('fas', 'fa-spinner', 'fa-spin');

    document.getElementById('recordButton').addEventListener('click', function () {
        document.getElementById('recordingTime').innerText = 'Recording...';

        // Start recording timer
        var seconds = 0; 
        recordingTimer = setInterval(function () {
            seconds++;
            document.getElementById('recordingTime').innerText = 'Recording: ' + seconds + ' seconds';
        }, 1000);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{{ url_for("record_audio") }}', true);

        xhr.onload = function () {
            clearInterval(recordingTimer);
            alert(JSON.parse(xhr.responseText).message);
            document.getElementById('recordingTime').innerText = 'Recording stopped';
        };

        xhr.onerror = function () {
            clearInterval(recordingTimer);
            alert('Error: ' + JSON.parse(xhr.responseText).error);
            document.getElementById('recordingTime').innerText = 'Recording stopped due to an error';
        };

        xhr.send();
    });

    document.getElementById('analyzeButton').addEventListener('click', function () {
        document.getElementById('analysisResult').innerText = '';

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '{{ url_for("analyze_audio") }}', true);

        xhr.onload = function () {
            clearInterval(recordingTimer);
            loadingIcon.remove();
            alert(JSON.parse(xhr.responseText).result);
            document.getElementById('recordingTime').innerText = 'Analysis completed';
            document.getElementById('analysisResult').innerText = JSON.parse(xhr.responseText).result;
        };

        xhr.onerror = function () {
            clearInterval(recordingTimer);
            loadingIcon.remove();
            alert('Error: ' + JSON.parse(xhr.responseText).error);
            document.getElementById('recordingTime').innerText = 'Analysis stopped due to an error';
            document.getElementById('analysisResult').innerText = 'Analysis failed';
        };

        xhr.send();
    });
});