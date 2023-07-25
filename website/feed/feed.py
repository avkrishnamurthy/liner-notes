from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from website.utils import date

feed_ = Blueprint('feed', __name__, template_folder='templates', static_url_path='feed/', static_folder='static')

@feed_.route('/feed')
@login_required
def feed():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    my_feed = current_user.feed.paginate(page=page, per_page=per_page)
    return render_template("feed.html", user=current_user, feed=my_feed, convert_datetime=date.convert_datetime, length=my_feed.pages)



