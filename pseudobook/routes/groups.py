from flask import Blueprint, flash, abort, jsonify
from flask import render_template, url_for, request, redirect 
from flask import jsonify
from flask_login import login_required, current_user
from urllib.parse import urlparse, urljoin

from pseudobook.database import mysql

from pseudobook.models import page as page_model
from pseudobook.models import group as group_model
from pseudobook.models import page as page_model
from pseudobook.models import post as post_model
from pseudobook.models import comment as comment_model
from pseudobook.models import like as like_model

from pseudobook.forms.create_group import CreateGroup as CreateGroupForm
from pseudobook.forms.join_unjoin_group import JoinUnjoinGroup as JoinUnjoinForm
from pseudobook.forms.rename_group import RenameGroup as RenameGroupForm
from pseudobook.forms.make_post import MakePost as MakePostForm
from pseudobook.forms.remove_post import RemovePost as RemovePostForm
from pseudobook.forms.edit_post import EditPost as EditPostForm
from pseudobook.forms.make_comment import MakeComment as MakeCommentForm
from pseudobook.forms.remove_comment import RemoveComment as RemoveCommentForm
from pseudobook.forms.edit_comment import EditComment as EditCommentForm
from pseudobook.forms.like_unlike import LikeUnlike as LikeUnlikeForm
from pseudobook.forms.delete_group import DeleteGroup as DeleteGroupForm

POSTS_PER_PAGE = 10
USERS_PER_PAGE = 15
GROUPS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('groups', __name__, template_folder='../templates/groups')

'''
View Routes
'''
@mod.route('/groups', methods=['GET'])
@login_required
def groups():
    groups_offset = request.values.get('groups_offset')
    groups_offset = int(groups_offset) if groups_offset else 0
    posts_offset = request.values.get('posts_offset')
    posts_offset = int(posts_offset) if posts_offset else 0

    total_groups = group_model.Group.count_groups(None)
    groups = group_model.Group.scroll_groups(groups_offset, GROUPS_PER_PAGE, None)
    prev_groups = True if groups_offset > 0 else False
    next_groups = True if ((groups_offset + 1) * GROUPS_PER_PAGE) < total_groups else False

    # Scroll all posts made in groups
    total_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_GROUP, None)
    posts = page_model.Page.scroll_posts_for_group_pages(posts_offset, POSTS_PER_PAGE, None)
    prev_posts = True if posts_offset > 0 else False
    next_posts = True if ((posts_offset + 1) * POSTS_PER_PAGE) < total_posts else False

    for group_post in posts:
        group_post.remove_post_form = RemovePostForm()
        group_post.user_has_liked = like_model.Like.user_has_liked(group_post.postID, current_user.userID, "po")
        group_post.like_count = like_model.Like.like_count(group_post.postID, "po")

        group_post.comments = group_post.get_comments()
        for comment in group_post.comments:
            comment.user_has_liked = like_model.Like.user_has_liked(comment.commentID, current_user.userID, "cm")
            comment.like_count = like_model.Like.like_count(comment.commentID, "cm")
        
    make_comment_form = MakeCommentForm()
    remove_comment_form = RemoveCommentForm()
    edit_post_form = EditPostForm()
    edit_comment_form = EditCommentForm()
    like_unlike_form = LikeUnlikeForm()
    return render_template('groups.html', 
                            current_user=current_user, 
                            groups=groups, 
                            prev_groups=prev_groups, 
                            next_groups=next_groups,
                            groups_offset=groups_offset,
                            posts=posts,
                            prev_posts=prev_posts,
                            next_posts=next_posts,
                            posts_offset=posts_offset,
                            make_comment_form=make_comment_form,
                            remove_comment_form=remove_comment_form,
                            edit_post_form=edit_post_form,
                            edit_comment_form=edit_comment_form,
                            like_unlike_form=like_unlike_form)

@mod.route('/group/<string:groupID>', methods=['GET'])
@login_required
def group_page(groupID):
    posts_offset = request.values.get('posts_offset')
    posts_offset = int(posts_offset) if posts_offset else 0

    users_offset = request.values.get('users_offset')
    users_offset = int(users_offset) if users_offset else 0

    addable_users_offset = request.values.get('addable_users_offset')
    addable_users_offset = int(addable_users_offset) if addable_users_offset else 0

    group = group_model.Group.get_group_by_id(groupID)
    if group:
        page = page_model.Page.get_page_by_group_id(groupID)

    total_posts = page.count_posts(None)
    posts = page.scroll_posts(posts_offset, POSTS_PER_PAGE, None)
    prev_posts = True if posts_offset > 0 else False
    next_posts = True if ((posts_offset + 1) * POSTS_PER_PAGE) < total_posts else False

    total_users = group.count_users(None)
    users = group.scroll_users(users_offset, USERS_PER_PAGE, None)
    prev_users = True if users_offset > 0 else False
    next_users = True if ((users_offset + 1) * USERS_PER_PAGE) < total_users else False

    total_addable_users = group.count_addable_users()
    addable_users = group.scroll_addable_users(addable_users_offset, USERS_PER_PAGE)
    prev_addable_users = True if addable_users_offset > 0 else False
    next_addable_users = True if ((addable_users_offset + 1) * USERS_PER_PAGE) < total_addable_users else False

    current_user_is_member = group.is_member(current_user.userID)
    current_user_is_owner = group.is_owner(current_user.userID)

    make_post_form = MakePostForm()
    make_comment_form = MakeCommentForm()
    edit_comment_form = EditCommentForm()
    remove_comment_form = RemoveCommentForm()
    edit_post_form = EditPostForm()
    join_unjoin_form = JoinUnjoinForm()
    rename_group_form = RenameGroupForm()
    delete_group_form = DeleteGroupForm()

    for post in posts:
        post.remove_post_form = RemovePostForm()
        group_post.user_has_liked = like_model.Like.user_has_liked(group_post.postID, current_user.userID, "po")
        post.like_count = like_model.Like.like_count(post.postID, "po")

        post.comments = post.get_comments()
        for comment in post.comments:
            comment.user_has_liked = like_model.Like.user_has_liked(comment.commentID, current_user.userID, "cm")
            comment.like_count = like_model.Like.like_count(comment.commentID, "cm")
            
    for user in users:
        user.join_unjoin_form = JoinUnjoinForm()
    for user in addable_users:
        user.join_unjoin_form = JoinUnjoinForm()
    return render_template('group_page.html', 
                            current_user=current_user, 
                            group=group,
                            page=page,
                            current_user_is_member=current_user_is_member,
                            current_user_is_owner=current_user_is_owner,
                            posts=posts,
                            prev_posts=prev_posts, 
                            next_posts=next_posts,
                            posts_offset=posts_offset,
                            users=users,
                            prev_users=prev_users,
                            next_users=next_users,
                            users_offset=users_offset,
                            addable_users=addable_users,
                            prev_addable_users=prev_addable_users,
                            next_addable_users=next_addable_users,
                            addable_users_offset=addable_users_offset,
                            make_post_form=make_post_form,
                            join_unjoin_form=join_unjoin_form,
                            rename_group_form=rename_group_form,
                            delete_group_form=delete_group_form,
                            make_comment_form=make_comment_form,
                            remove_comment_form=remove_comment_form,
                            edit_post_form=edit_post_form,
                            edit_comment_form=edit_comment_form)

@mod.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create():
    create_group_form = CreateGroupForm()
    return render_template('create.html', form=create_group_form)

'''
Form Routes
'''
@mod.route('/groups/forms/create', methods=['POST'])
def create_group_form():
    groupName = request.form['groupName']

    create_group_form = CreateGroupForm(request.form)

    if request.form and create_group_form.validate_on_submit():
        new_group = group_model.Group(None, groupName, current_user.userID)
        try:
            new_group.groupID = new_group.create_group()
        except (mysql.connection.Error, mysql.connection.Warning) as e:
                print("Exeption of type {} occured: {}".format(type(e), e))
        else:
                return redirect(url_for('groups.group_page', groupID=new_group.groupID))

        return redirect(url_for('groups.create'))
    else:
        flash('There was an error in group creation. Please try again.')
        return redirect(url_for('groups.create'))

'''
Form Routes
'''
@mod.route('/groups/forms/make_post', methods=['POST'])
@login_required
def make_post_form():
    content = request.form['content']
    pageID = request.form['pageID']
    authorID = current_user.userID
    page = page_model.Page.get_page_by_id(pageID)

    make_post_form = MakePostForm(request.form)
    if request.form and make_post_form.validate_on_submit():
        try:
            postID = page.post_to_page(content, authorID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error posting to this page.')
    else:
        flash('There was an error posting to this page.')

    return redirect(request.referrer)

@mod.route('/groups/forms/remove_post', methods=['POST'])
@login_required
def remove_post_form():
    postID = request.form['postID']

    remove_post_form = RemovePostForm(request.form)
    if request.form and remove_post_form.validate_on_submit():
        # Only allow user who owns page to delete a post on that page
        post = post_model.Post.get_post_by_id(postID)
        page = page_model.Page.get_page_by_id(post.pageID)
        if page.pageType == page_model.Page.PAGE_TYPE_GROUP:
            if current_user.userID == post.authorID:
                try:
                    post_model.Post.remove_post(postID)
                except (mysql.connection.Error, mysql.connection.Warning) as e:
                    print(e)
                    # Print custom error message
                    if e.args[0] == 1644:
                        flash(e.args[1])
                    else:
                        flash('There was an error removing this post.')
            else:
                abort(403)
    else:
        flash('There was an error removing this post.')

    return redirect(request.referrer)

@mod.route('/groups/forms/edit_post_form', methods=['POST'])
@login_required
def edit_post_form():
    content = request.form['content']
    postID = request.form['postID']

    post = post_model.Post.get_post_by_id(postID)
    edit_post_form = EditPostForm(request.form)
    if request.form and edit_post_form.validate_on_submit():
        try:
            post.edit_post(content)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error editing this post.')
        
        return jsonify()
    else:
        flash('There was an error editing this post.')

    return abort(400, 'There was an error editing this post.')

@mod.route('/groups/forms/join_group', methods=['POST'])
@login_required
def join_group():
    groupID = request.form['groupID']
    userID = request.form['userID']

    join_unjoin_form = JoinUnjoinForm(request.form)
    if request.form and join_unjoin_form.validate_on_submit():
        group = group_model.Group.get_group_by_id(groupID)
        try:
            group.join_group(userID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error joining this group.')
    else:
        flash('There was an error joining this group.')

    return redirect(request.referrer)

@mod.route('/groups/forms/unjoin_group', methods=['POST'])
@login_required
def unjoin_group():
    groupID = request.form['groupID']
    userID = request.form['userID']

    join_unjoin_form = JoinUnjoinForm(request.form)
    if request.form and join_unjoin_form.validate_on_submit():
        group = group_model.Group.get_group_by_id(groupID)
        try:
            group.unjoin_group(userID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error unjoining this group.')
    else:
        flash('There was an error unjoining this group.')

    return redirect(request.referrer)

@mod.route('/groups/forms/delete_group', methods=['POST'])
@login_required
def delete_group():
    groupID = request.form['groupID']
    userID = request.form['userID']
    cursor = mysql.connection.cursor()
    try:
        query = '''CALL deleteGroup({0}, {1})
                '''.format(current_user.userID, groupID) 
        cursor.execute(query)
        mysql.connection.commit()
    except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
    return redirect(url_for('groups.groups'))

@mod.route('/groups/forms/rename_group', methods=['POST'])
@login_required
def rename_group():
    groupID = request.form['groupID']
    groupName = request.form['content']
    cursor = mysql.connection.cursor()
    try:
        query = '''CALL renameGroup({0}, {1}, "{2}")
                '''.format(current_user.userID, groupID, groupName) 
        cursor.execute(query)
        mysql.connection.commit()
    except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
    return redirect(request.referrer)

@mod.route('/groups/forms/make_comment', methods=['POST'])
@login_required
def make_comment():
    postID = request.form['postID']
    content = request.form['content']
    authorID = request.form['authorID']

    make_comment_form = MakeCommentForm(request.form)
    if request.form and make_comment_form.validate_on_submit():
        post = post_model.Post.get_post_by_id(postID)
        try:
            commentID = post.make_comment(content, authorID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error commenting on this post.')
        else:
            comment = comment_model.Comment.get_comment_by_id(commentID)
            return render_template('comment.html', 
                                    comment=comment)
    else:
        flash('There was an error commenting on this post.')

    return abort(400, 'There was an error commenting on this post.')

@mod.route('/groups/forms/remove_comment', methods=['POST'])
@login_required
def remove_comment():
    commentID = request.form['commentID']

    remove_comment_form = RemoveCommentForm(request.form)
    if request.form and remove_comment_form.validate_on_submit():
        # Only allow user who owns comment to delete it 
        comment = comment_model.Comment.get_comment_by_id(commentID)
        if current_user.userID == comment.authorID:
            try:
                comment_model.Comment.remove_comment(commentID)
            except (mysql.connection.Error, mysql.connection.Warning) as e:
                print(e)
                # Print custom error message
                if e.args[0] == 1644:
                    flash(e.args[1])
                else:
                    flash('There was an error removing this comment.')

            return jsonify()
        else:
            abort(403)
    else:
        flash('There was an error removing this comment.')

    return abort(400, 'There was an error removing this comment.')

@mod.route('/groups/forms/edit_comment_form', methods=['POST'])
@login_required
def edit_comment_form():
    content = request.form['content']
    commentID = request.form['commentID']

    comment = comment_model.Comment.get_comment_by_id(commentID)
    edit_comment_form = EditCommentForm(request.form)
    if request.form and edit_comment_form.validate_on_submit():
        try:
            comment.edit_comment(content)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error editing this comment.')
        
        return jsonify()
    else:
        flash('There was an error editing this comment.')

    return abort(400, 'There was an error editing this comment.')

@mod.route('/likes/forms/like_unlike', methods=['POST'])
@login_required
def like_unlike():
    parentID = request.form['parentID']
    authorID = request.form['authorID']
    contentType = request.form['contentType']

    user_has_liked = like_model.Like.user_has_liked(parentID, authorID, contentType)
    if user_has_liked:
        like_model.Like.unlike(parentID, authorID, contentType)
        user_has_liked = False
    else:
        like_model.Like.like(parentID, authorID, contentType)
        user_has_liked = True

    if contentType == 'po':
        post = post_model.Post.get_post_by_id(parentID)
        post.user_has_liked = user_has_liked
        
        return render_template('like.html',
                                post=post)
    elif contentType == 'cm':
        comment = comment_model.Comment.get_comment_by_id(parentID)
        comment.user_has_liked = user_has_liked
        
        return render_template('like.html',
                                comment=comment)
    else:
        return abort(400, 'There was an error liking/unliking.')
