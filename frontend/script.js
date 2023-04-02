async function handleClick() {
  img = document.getElementById("img-upload").files[0];
  if (img) {
    imgTextEl = document.getElementById("img-text");
    textValue = imgTextEl.value;
    if (!textValue || textValue.split(" ").length > 3) {
      alert("Fill in text or keep within 3 words");
      return;
    }

    let formData = new FormData();
    formData.append("img", img);
    formData.append("imgText", textValue);
    imgTextEl.value = "Loading...";

    try {
      let response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        mode: "no-cors",
        body: formData,
      });

      let data = await response.blob();
      if (data && data.size > 0) {
        const url = URL.createObjectURL(data);
        let a = document.createElement("a");
        a.download = "thumbnail.png";
        a.href = url;
        a.click();
      }
    } catch (error) {
      console.log(error);
    } finally {
      imgTextEl.value = "";
    }
  }
}
