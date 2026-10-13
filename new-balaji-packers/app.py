from flask import Flask, render_template, request, redirect, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html', C=Config, B=Config)

@app.route('/about')
def about():
    return render_template('about.html', C=Config)

@app.route('/contact')
def contact():
    return render_template('contact.html', C=Config)

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        pickup = request.form.get('pickup_city')
        drop = request.form.get('drop_city')
        items = request.form.getlist('items')
        custom_items = request.form.get('custom_items')
        
        print(f"New Order from {name} ({phone}): From {pickup} to {drop}. Items: {items}, Extra: {custom_items}")
        return render_template('thanks.html', name=name, C=Config)
        
    return render_template('quote.html', C=Config)

@app.route('/submit-review', methods=['POST'])
def submit_review():
    reviewer = request.form.get('reviewer_name')
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    print(f"New Review from {reviewer} ({rating} stars): {review_text}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)