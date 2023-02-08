from flask import Flask,render_template,Response,request
import Checksum
app = Flask(__name__)
MERCHANT_KEY = 'txD2tlHax&ls%3pt'
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/start')
def start():
    param_dict = {

                'MID': 'obQIPX90562701803310',
                'ORDER_ID': '21',
                'TXN_AMOUNT': '1',
                'CUST_ID': 'pradeepsaini384@gmail.com',
                'INDUSTRY_TYPE_ID': 'WEBSTAGING',
                'WEBSITE': 'Retail',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:5000/paymentstatus',

        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render_template('paytm.html', param_dict= param_dict)

@app.route('/paymentstatus',methods=['GET','POST'])
def paymentstatus():
    # paytm will send you post request here
    form = request.form.to_dict()
    print(form)
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render_template('paymentstatus.html', response= response_dict)


if __name__ == '__main__':
    app.run(debug=True)