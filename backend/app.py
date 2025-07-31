from flask import Flask, render_template, request, send_file, session
import pickle, os
from generate_pdf import generate_pdf



app = Flask(__name__)
app.secret_key = 'autism_app_secret'

# Load the trained Random Forest model
model_path = os.path.join(os.path.dirname(__file__), '..', 'ml_model', 'random_forest_model.pkl')
model = pickle.load(open(model_path, 'rb'))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/form')
def form():
    question_texts = {
        1: "Does your child respond to their name when you call them?",
        2: "Does your child make eye contact when interacting with you or others?",
        3: "Does your child point at things to show interest?",
        4: "Does your child avoid playing or interacting with other children?",
        5: "Does your child repeat certain movements or behaviors?",
        6: "Does your child get very upset by small changes in routines?",
        7: "Does your child show unusual sensitivity to sounds, lights, textures, or smells?",
        8: "Does your child focus more on objects than people?",
        9: "Does your child have delayed speech or very limited language for their age?",
        10: "Does your child avoid using gestures like waving or nodding?"
    }

    question_tips = {
        1: "Lack of response can be an early sign of social communication delay.",
        2: "Poor eye contact is one of the most common early signs of autism.",
        3: "Lack of pointing by 18 months is a red flag in autism screenings.",
        4: "Social disengagement from peers is a core autism trait.",
        5: "Examples include hand-flapping, rocking, or spinning.",
        6: "Insistence on sameness is common in autism spectrum conditions.",
        7: "Sensory sensitivities are often strong indicators.",
        8: "This may reflect restricted interests or atypical focus.",
        9: "Language delay is often one of the earliest concerns noticed by parents.",
        10: "Gesture use is a developmental milestone often impaired in ASD."
    }

    return render_template('form.html', question_texts=question_texts, question_tips=question_tips)



@app.route('/predict', methods=['POST'])
def predict():
    try:

        parent_name = request.form['parent_name']
        child_name = request.form['child_name']
        age = int(request.form['age'])
        gender = int(request.form['gender'])
        jaundice = int(request.form['jaundice'])
        austim = int(request.form['austim'])
        used_app = int(request.form['used_app'])
        
        # Get Q1–Q10 answers from form
        q_answers = [int(request.form[f'Q{i}']) for i in range(1, 11)]

        # Ensure feature length matches model input (19 features total)
        features = [age, gender, jaundice, austim, used_app] + q_answers + [0, 0, 0, 0]

        prediction = model.predict([features])[0]
        confidence = model.predict_proba([features])[0][1] * 100
        confidence = round(confidence, 2)

        if prediction == 1:
            result = "Likely Autistic"
            suggestion = (
                "Please consult a pediatric psychologist for further assessment. "
                "Meanwhile, early intervention strategies like structured play, speech therapy, "
                "and social interaction activities can be helpful."
    )
        else:
            result = "Unlikely Autistic"
            suggestion = (
                "No major signs observed, but continue monitoring your child's development. "
                "Engage them in regular communication, reading, and age-appropriate play to support growth."
    )


        # Save results to session
        session['result'] = result
        session['suggestion'] = suggestion
        session['parent_name'] = parent_name
        session['child_name'] = child_name
        session['confidence'] = confidence
       

        return render_template("result.html", result=result, suggestion=suggestion,parent_name=parent_name, child_name=child_name,confidence=confidence)

    except Exception as e:
        return f"Error during prediction: {str(e)}"

@app.route('/download_pdf')
def download_pdf():
    result = session.get('result')
    suggestion = session.get('suggestion')

    if not result or not suggestion:
        return "No result data available. Please complete the form first."

    pdf_path = generate_pdf(result, suggestion, parent_name=session.get('parent_name'),
    child_name=session.get('child_name'),
    confidence=session.get('confidence'))
    return send_file(pdf_path, as_attachment=True)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')





if __name__ == '__main__':
    app.run(debug=True)
