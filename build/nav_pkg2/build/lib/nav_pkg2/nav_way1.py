# RViz의 "Nav2 Goal" 버튼을 대체하고 Waypoint를 지정하는 코드
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import math

def make_pose(navigator, x, y, yaw=0.0):
    # x, y : 맵 좌표
    # yaw : 로보이 도착해서 바라볼 방향(rad)

    pose = PoseStamped()

    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()

    # 위치
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0

    # yaw -> 쿼터니언
    pose.pose.orientation.z = 0.0
    pose.pose.orientation.w = 0.0
    pose.pose.orientation.z = math.sin(yaw/2.0)
    pose.pose.orientation.w = math.cos(yaw/2.0)

    return pose

def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    #1. 초기 위치
    # Gazebo spawn 위치 (0, 0)를 사용
    initial_pose = make_pose(
        navigator,
        0.0,
        0.0,
        0.0
    )

    navigator.setInitialPose(initial_pose)

    #2. Nav2 활성화 대기
    navigator.waitUntilNav2Active()

    #3. waypoints 작성
    '''
    x: 0.2808151841163635
    y: -1.3340572118759155
    z: 0.002471923828125

    x: 0.7474057674407959
    y: -0.4822501540184021
    z: 0.002471923828125
    '''
    waypoints = [
        # waypoint 1
        make_pose(
            navigator,
            0.2,
            -1.3,
            0.0
        ),

        # waypoint 2
        make_pose(
            navigator,
            0.7,
            -0.4,
            math.pi/2.0
        ),

    ]

    #4. waypoint 실행
    navigator.followWaypoints(waypoints)

    #5. 완료까지 대기
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback is not None:
            navigator.get_logger().info(
                'Waypoint 주행 중...'
            )

    #6. 결과 확인
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info(
            "모든 경유지 이동 성공"
        )

    elif result == TaskResult.CANCELED:
        navigator.get_logger().info(
            "Waypoint 이동 취소"
        )

    elif result == TaskResult.FAILED:
        navigator.get_logger().info(
            "Waypoint 이동 실패"
        )

    else:
        navigator.get_logger().info(
            "알 수 없는 결과"
        )

    rclpy.shutdown()

if __name__=='__main__':
    main()