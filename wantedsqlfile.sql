
SELECT t.user_id, m.message_id FROM target_follower t LEFT OUTER JOIN MESSAGES m on m.user_id=t.user_id;

SELECT distinct m.user_id FROM target_follower t RIGHT OUTER JOIN MESSAGES m on m.user_id=t.user_id where m.user_id!='' and t.user_id is NULL;

SELECT distinct m.user_id, m.user_code FROM target_follower t RIGHT OUTER JOIN MESSAGES m on m.user_id=t.user_id where m.user_id!='' and t.user_id is NULL;

-- Populate Target Followers out of Messages
insert into user_follow (user_id,user_code, status)
SELECT distinct m.user_id, m.user_code, '1' as status FROM user_follow f RIGHT OUTER JOIN MESSAGES m on m.user_id=f.user_id where m.user_id!='' and f.user_id is NULL

insert into user_group (user_id,group_id)
select user_id, '1' as group_id from target_follower where status='0'

SELECT m.message_id FROM message m
left outer join message_retweet r on r.message_id=m.message_id 
where r.message_id is NULL

-- Populate Targets for Likes
insert into message_like (message_id, status)
SELECT m.message_id, '1' as status FROM message m
left outer join message_like ml on ml.message_id=m.message_id 
where ml.message_id is NULL

-- Populate Targets for Retweets
insert into message_retweet (message_id, status)
SELECT m.message_id, '1' as status FROM message m
left outer join message_retweet r on r.message_id=m.message_id 
where r.message_id is NULL

insert into users (user_id, user_code)

SELECT distinct m.user_id, m.user_code
FROM message m left outer join users u on u.user_id=m.user_id
where u.user_id is NULL

insert into users (user_id, user_code)
SELECT distinct m.user_id, m.user_code FROM message m left outer join users u on u.user_id=m.user_id where u.user_id is NULL;

insert into message_like (message_id, status)
SELECT m.message_id, '1' as status 
FROM message m
left outer join message m on m.message_id=m.message_id 
where ml.message_id is NULL
