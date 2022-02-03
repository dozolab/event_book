# routes.py
import pathlib

from .views import person_list, event_list, coupon_list, login


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', person_list, name='person_list_with_more_than_three_events')
    app.router.add_get('/events', event_list, name='event_list')
    app.router.add_post('/login', login, name='event_list_login')
    app.router.add_get('/coupons', coupon_list, name='coupon_list')
