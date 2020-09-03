"""empty message

Revision ID: 32aabb57f0df
Revises: 
Create Date: 2020-09-04 03:31:12.410884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32aabb57f0df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_list',
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.PrimaryKeyConstraint('channel_id')
    )
    op.create_index(op.f('ix_channel_list_channel_id'), 'channel_list', ['channel_id'], unique=True)
    op.create_table('channel_playlist_items',
    sa.Column('video_id', sa.String(length=11), nullable=False),
    sa.Column('video_published_at', sa.DateTime(), nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.PrimaryKeyConstraint('video_id')
    )
    op.create_table('top_level_comment',
    sa.Column('comment_id', sa.String(length=26), nullable=False),
    sa.Column('video_id', sa.String(length=11), nullable=False),
    sa.Column('text_original', sa.String(), nullable=False),
    sa.Column('author_display_name', sa.String(), nullable=False),
    sa.Column('author_channel_id', sa.String(), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('channel_content_detail',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.Column('channel_related_playlists', sa.String(length=24), nullable=False),
    sa.Column('channel_keywords', sa.JSON(), nullable=True),
    sa.Column('channel_topic_id', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_keywords',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.Column('keyword', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_snippet',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.Column('channel_title', sa.String(length=100), nullable=False),
    sa.Column('channel_description', sa.String(length=1000), nullable=False),
    sa.Column('channel_custom_url', sa.String(length=100), nullable=False),
    sa.Column('channel_published_at', sa.DateTime(), nullable=False),
    sa.Column('channel_thumbnails_url', sa.String(length=200), nullable=False),
    sa.Column('channel_country', sa.String(length=2), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_statist',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.Column('view_count', sa.BIGINT(), nullable=False),
    sa.Column('comment_count', sa.BIGINT(), nullable=False),
    sa.Column('subscriber_count', sa.BIGINT(), nullable=False),
    sa.Column('video_count', sa.BIGINT(), nullable=False),
    sa.Column('hidden_subscriber_count', sa.BOOLEAN(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_topic',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('channel_id', sa.String(length=24), nullable=False),
    sa.Column('topic_name', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('replies_comments',
    sa.Column('comments_id', sa.String(length=49), nullable=False),
    sa.Column('parent_id', sa.String(length=26), nullable=False),
    sa.Column('video_id', sa.String(length=11), nullable=False),
    sa.Column('text_original', sa.String(), nullable=False),
    sa.Column('author_display_name', sa.String(), nullable=False),
    sa.Column('author_channel_id', sa.String(), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['top_level_comment.comment_id'], ),
    sa.PrimaryKeyConstraint('comments_id', 'parent_id')
    )
    op.create_table('subscriptions',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('resource_channel_id', sa.String(length=24), nullable=False),
    sa.Column('original_channel_id', sa.String(length=24), nullable=False),
    sa.Column('subscript_at', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['original_channel_id'], ['channel_list.channel_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_resource_channel_id'), 'subscriptions', ['resource_channel_id'], unique=True)
    op.create_table('video_detail',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('video_id', sa.String(length=11), nullable=False),
    sa.Column('title', sa.String(length=70), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=False),
    sa.Column('category_id', sa.SMALLINT(), nullable=False),
    sa.Column('default_audio_language', sa.String(length=5), nullable=False),
    sa.Column('live_broadcast_content', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['video_id'], ['channel_playlist_items.video_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('video_statistics',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('video_id', sa.String(length=11), nullable=False),
    sa.Column('view_count', sa.BIGINT(), nullable=False),
    sa.Column('like_count', sa.BIGINT(), nullable=False),
    sa.Column('dislike_count', sa.BIGINT(), nullable=False),
    sa.Column('favorite_count', sa.BIGINT(), nullable=False),
    sa.Column('comment_count', sa.BIGINT(), nullable=False),
    sa.ForeignKeyConstraint(['video_id'], ['channel_playlist_items.video_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video_statistics')
    op.drop_table('video_detail')
    op.drop_index(op.f('ix_subscriptions_resource_channel_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_table('replies_comments')
    op.drop_table('channel_topic')
    op.drop_table('channel_statist')
    op.drop_table('channel_snippet')
    op.drop_table('channel_keywords')
    op.drop_table('channel_content_detail')
    op.drop_table('top_level_comment')
    op.drop_table('channel_playlist_items')
    op.drop_index(op.f('ix_channel_list_channel_id'), table_name='channel_list')
    op.drop_table('channel_list')
    # ### end Alembic commands ###
