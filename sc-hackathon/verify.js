let postIndex = 0;
const images = ["https://cdn.sharechat.com/36a30d87_1668669326320_sc.jpeg",
    "https://cdn.sharechat.com/11c338e1_1663661009057_sc.jpeg",
    "https://cdn.sharechat.com/1434397_1663660969761_sc.jpeg",
    "https://cdn.sharechat.com/35e1fdff_1663341668273_sc.jpeg",
    "https://cdn.sharechat.com/2c82401a-9e25-44f2-a46b-4d11701131c3-f48e3b15-d3ec-4c46-b09f-40dc09389bcc.jpeg",
    "https://cdn.sharechat.com/34bdf39b_1663217741242_sc.jpeg"]
document.addEventListener("DOMContentLoaded", function () {
    var video = document.getElementById('video'); // Video

    var canvas = document.querySelector('canvas');
    var context = canvas.getContext('2d');
    var image = document.querySelector('img');
    var w, h, ratio;

    //add loadedmetadata which will helps to identify video attributes

    video.addEventListener('loadedmetadata', function () {
        ratio = video.videoWidth / video.videoHeight;
        w = video.videoWidth - 100;
        h = parseInt(w / ratio, 10);
        canvas.width = w;
        canvas.height = h;

    }, false);



    // Stream Camera To Video Element
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            }).catch(function (error) {
                console.log(error)
            })
    }


    function takeActionLogic() {
        context.fillRect(0, 0, w, h);
        context.drawImage(video, 0, 0, w, h);
        var dataURI = canvas.toDataURL('image/jpeg');
        console.log(dataURI)
        image.src = images[(postIndex) % images.length]
        postIndex++;

        (async () => {
            emotion.innerHTML = `Emotion Loading...`
            const rawResponse = await fetch('http://localhost:5000/isDrowsy', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({ dataURI })
            });
            const content = await rawResponse.json();
            const isClosed = content == '1';
            const sleepyText = 'Drowsy';
            const awakeText = 'Awake';
            console.log("CONTENT::::", content)
            if (isClosed) {
                emotion.innerHTML = `Emotion: ${sleepyText}`
                alert(`Please Focus. Your emotion is detected as Emotion ${sleepyText}`)
            } else {
                emotion.innerHTML = `Emotion: ${awakeText}`
            }


        })();

    }


    // On Take Action Button Click
    document.getElementById('discard').addEventListener('click', takeActionLogic )
    document.getElementById('accept').addEventListener('click', takeActionLogic )



});
