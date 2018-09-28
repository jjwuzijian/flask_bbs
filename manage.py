#endcoding: utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_bbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.fromt import models as fromt_models

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmission

FrontUser = fromt_models.FrontUser

app = create_app()
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_role():
    #访问者
    visitor = CMSRole(name='visitor',desc='只能修改个人信息和查看权限')
    visitor.permissons = CMSPermission.VISITOR
    #修改个人信息和管理帖子，管理评论，管理前台用户
    operator = CMSRole(name='operator',desc='管理帖子,管理评论,管理前台用户')
    operator.permissons = CMSPermission.VISITOR|CMSPermission.COMMENTER|CMSPermission.POSTER|CMSPermission.FRONTUSER
    #管理员
    admin = CMSRole(name='admin',desc='管理员')
    admin.permissons = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.BOARDER|CMSPermission.FRONTUSER|CMSPermission.CMSUSER
    #超级管理员
    developer = CMSRole(name='developer',desc='超级管理员')
    developer.permissons = CMSPermission.ALL_PERMISSON

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色")
        else:
            print('没有这个角色：{0}'.format(role))
    else:
        print("{0}邮箱没有这个用户".format(email))

@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('有访问者权限')
    else:
        print('你没有访问者权限')

if __name__ == "__main__":
    manager.run()
