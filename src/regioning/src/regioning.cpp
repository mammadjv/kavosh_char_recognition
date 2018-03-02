#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>
#include <vector>
#include <system_messages/Image.h>
#include <std_msgs/Bool.h>


using namespace std;
using namespace ros;
using namespace cv;

class Image_Publisher_Subscriber{
public:
	ros::Publisher contour_publisher;

//	ros::Subscriber image_subscriber;

	image_transport::ImageTransport *it;
	image_transport::Subscriber image_subscriber;

	ros::Publisher life_cycle_state_publisher;
	cv_bridge::CvImagePtr cv_ptr;

	Image_Publisher_Subscriber(ros::NodeHandle nh){
		
		contour_publisher = nh.advertise <system_messages::Image>("/contours",1);
		it = new image_transport::ImageTransport(nh);
		image_subscriber = it->subscribe("/image", 1, &Image_Publisher_Subscriber::on_image_received, this);
		life_cycle_state_publisher = nh.advertise <std_msgs::Bool>("/life_cycle_state",1);
//		image_subscriber = nh.subscribe("/image", 1, &Image_Publisher_Subscriber::on_image_received, this);
	}

	void on_image_received(const sensor_msgs::ImageConstPtr& msg){
		cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
		cv::Mat image  = cv_ptr->image;
		Mat contour;
		bool has_contour = this->calc_contours(image,contour);
		this->publish(has_contour , contour);
	}

	bool calc_contours(Mat image, Mat &contour){
		// algorithm
		contour = image;
		return true;
	}

	void publish(bool has_contour , Mat contour){
		if(has_contour == false){
			std_msgs::Bool life_cycle_ended;
			life_cycle_ended.data = true;
			life_cycle_state_publisher.publish(life_cycle_ended);
			return;
		}
		system_messages::Image::Ptr contour_msg = boost::make_shared<system_messages::Image>();
		contour_msg->image_is_prepared = has_contour;
		sensor_msgs::ImagePtr image_msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", contour).toImageMsg();
		contour_msg->rgb = *image_msg;
		contour_publisher.publish(contour_msg);
	}
};


int main(int argc, char **argv){

    std::string nodeName = "regioning_node";
    ros::init(argc, argv, nodeName);

    ros::NodeHandle nh;
    Image_Publisher_Subscriber* image_pub_sub = new Image_Publisher_Subscriber(nh);
    ros::spin();
}

