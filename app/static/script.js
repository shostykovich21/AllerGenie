    // // app/static/script.js
    // document.getElementById('submitBtn').onclick = async () => {
    // const imgFile = document.getElementById('imgInput').files[0];
    // const text    = document.getElementById('symptomText').value;

    // if (!imgFile) {
    //     alert("Please upload an image.");
    //     return;
    // }

    // // metadata
    // const meta = {
    //     age:      parseFloat(document.getElementById('age').value)  || 0.0,
    //     diameter_1: parseFloat(document.getElementById('diameter_1').value) || 0.0,
    //     diameter_2: parseFloat(document.getElementById('diameter_2').value) || 0.0,
    //     gender_M: parseFloat(document.getElementById('gender_M').value)
    // };
    // document.querySelectorAll('input[name="region"]').forEach(el => {
    //     meta[el.value] = el.checked ? 1.0 : 0.0;
    // });

    // const form = new FormData();
    // form.append('image', imgFile);
    // form.append('symptom_text', text);
    // form.append('metadata', JSON.stringify(meta));

    // const resp = await fetch('/api/infer', { method:'POST', body: form });
    // if(!resp.ok) { alert(resp.statusText); return; }
    // const { diagnosis, confidence, followup } = await resp.json();

    // document.getElementById('diagnosis').innerText  = `Diagnosis: ${diagnosis}`;
    // document.getElementById('confidence').innerText = `Confidence: ${(confidence*100).toFixed(1)}%`;
    // document.getElementById('followup').innerText   = `Follow-up: ${followup}`;
    // document.getElementById('results').hidden = false;
    // };
// app/static/script.js

// async function callInfer(payload) {
//   const resp = await fetch('/api/infer', { method:'POST', body: payload });
//   if (!resp.ok) throw new Error(resp.statusText);
//   return resp.json();
// }

// document.getElementById('submitBtn').onclick = async () => {
//   const imgFile = document.getElementById('imgInput').files[0];
//   const text    = document.getElementById('symptomText').value.trim();

//   if (!imgFile) {
//     alert("Please upload an image.");
//     return;
//   }

//   // gather metadata
//   const meta = {
//     age:        parseFloat(document.getElementById('age').value)      || 0.0,
//     diameter_1: parseFloat(document.getElementById('diameter_1').value) || 0.0,
//     diameter_2: parseFloat(document.getElementById('diameter_2').value) || 0.0,
//     gender_M:   parseFloat(document.getElementById('gender_M').value)
//   };

//   // region checkboxes
//   document.querySelectorAll('input[name="region"]').forEach(el => {
//     meta[el.value] = el.checked ? 1.0 : 0.0;
//   });

//   // build form
//   const form = new FormData();
//   form.append('image', imgFile);
//   form.append('symptom_text', text);
//   form.append('metadata', JSON.stringify(meta));

//   try {
//     const { diagnosis, confidence, followup } = await callInfer(form);

//     // render results
//     document.getElementById('diagnosis').innerText  = `Diagnosis: ${diagnosis}`;
//     document.getElementById('confidence').innerText = `Confidence: ${(confidence*100).toFixed(1)}%`;
//     document.getElementById('followupQuestion').innerText = `🔹 ${followup}`;

//     // show follow-up answer area
//     document.getElementById('followupAnswerBlock').hidden = false;
//     document.getElementById('results').hidden = false;

//   } catch (err) {
//     alert("Error: " + err.message);
//   }
// };

// // when user submits their follow-up answer…
// document.getElementById('submitFollowup').onclick = async () => {
//   const answer = document.getElementById('followupAnswer').value.trim();
//   if (!answer) {
//     alert("Please enter your follow-up answer.");
//     return;
//   }

//   // here you could send that back to another endpoint, or
//   // simply display a “thanks” message:
//   alert("Thanks for your answer!");
//   // optionally hide the follow-up block
//   document.getElementById('followupAnswerBlock').hidden = true;
// };
// app/static/script.js

const submitBtn = document.getElementById('submitBtn');
const submitFollowupBtn = document.getElementById('submitFollowup');

async function doDiagnosis() {
  // 1) Validate symptom text (required)
  const symptomEl = document.getElementById('symptomText');
  const symptomText = symptomEl.value.trim();
  if (!symptomText) {
    alert("Please describe your symptoms.");
    symptomEl.focus();
    return;
  }

  // 2) Get optional image
  const imgInput = document.getElementById('imgInput');
  const imgFile = imgInput.files[0];

  // 3) Build metadata object
  const meta = {
    age:        parseFloat(document.getElementById('age').value)      || 0.0,
    diameter_1: parseFloat(document.getElementById('diameter_1').value) || 0.0,
    diameter_2: parseFloat(document.getElementById('diameter_2').value) || 0.0,
    gender_M:   parseFloat(document.getElementById('gender_M').value)   || 0.0,
  };
  document.querySelectorAll('input[name="region"]').forEach(el => {
    meta[el.value] = el.checked ? 1.0 : 0.0;
  });

  // 4) Package into FormData
  const form = new FormData();
  if (imgFile) form.append('image', imgFile);
  form.append('symptom_text', symptomText);
  form.append('metadata', JSON.stringify(meta));

  // 5) Call backend
  try {
    const resp = await fetch('/api/infer', { method: 'POST', body: form });
    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(errText || resp.statusText);
    }
    const { diagnosis, confidence, followup } = await resp.json();

    // 6) Render results
    document.getElementById('diagnosis').innerText      = `Diagnosis: ${diagnosis}`;
    document.getElementById('confidence').innerText     = `Confidence: ${(confidence*100).toFixed(1)}%`;
    document.getElementById('followupQuestion').innerText = `🔹 ${followup}`;

    // 7) Show results & follow-up answer block
    document.getElementById('results').classList.remove('hidden');
    document.getElementById('followupAnswerBlock').classList.remove('hidden');

  } catch (err) {
    console.error(err);
    alert("Error during inference: " + err.message);
  }
}

function doFollowup() {
  const answerEl = document.getElementById('followupAnswer');
  const answer = answerEl.value.trim();
  if (!answer) {
    alert("Please enter your follow-up answer.");
    answerEl.focus();
    return;
  }
  // in a more advanced version you'd POST this to the backend…
  alert("Thanks for your answer!");
  // then hide just the follow-up answer UI
  document.getElementById('followupAnswerBlock').classList.add('hidden');
}

submitBtn.addEventListener('click', doDiagnosis);
submitFollowupBtn.addEventListener('click', doFollowup);
