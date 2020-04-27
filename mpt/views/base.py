from flask import jsonify, request, abort
from mpt.models import db


def insert(model):
    isSuccessful = True

    try:
        model.insert()
    except e:
        db.session.rollback()
        isSuccessful = False
    finally:
        if isSuccessful:
            return jsonify({
                'success': True,
                'created':  model.id,
            })
        else:
            abort(422)


def get_all(model, return_list_name):

    data = model.all()

    if data is None:
        abort(404)

    return jsonify({
        'success': True,
        return_list_name: [row._asdict() for row in data]
    })


def get_one(model, return_result_name):

    data = model.one_or_none()

    if data is None:
        abort(404)

    return jsonify({
        'success': True,
        return_result_name: data._asdict()
    })


def update(model, return_result_name):
    isSuccessful = True

    try:
        model.update()
    except e:
        db.session.rollback()
        isSuccessful = False
    finally:
        if isSuccessful:
            return jsonify({
                'success': True,
                return_result_name: model._asdict()
            })
        else:
            abort(422)


def delete(model):
    isSuccessful = True

    try:
        model.delete()
    except e:
        db.session.rollback()
        isSuccessful = False
    finally:
        if isSuccessful:
            return jsonify({
                'success': True
            })
        else:
            abort(422)
