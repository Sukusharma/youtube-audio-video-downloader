function downloadVideo() {
    let url = document.getElementById("video-url").value;
    let format = document.getElementById("format").value;
    let startTime = document.getElementById("start-time").value;
    let endTime = document.getElementById("end-time").value;

    fetch('/download', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url, format: format, startTime: startTime,  // 🚀 Sending trim start time
            endTime: endTime  })
    })
    .then(response => response.blob())
    .then(blob => {
        let link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "download." + format;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    })
    .catch(error => console.error("Error:", error));
}
