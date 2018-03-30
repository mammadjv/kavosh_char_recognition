#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>
#include <vector>
#include <system_messages/ImageMsg.h>
#include <std_msgs/Bool.h>


using namespace std;
using namespace ros;
using namespace cv;

class Image_Publisher_Subscriber{
public:

	ros::Publisher contour_publisher;
	ros::Subscriber image_subscriber;
	ros::Subscriber bool_subscriber;
	ros::Publisher life_cycle_state_publisher;
	cv_bridge::CvImagePtr cv_ptr;
	Image_Publisher_Subscriber(ros::NodeHandle nh){
		
		contour_publisher = nh.advertise <system_messages::ImageMsg>("/contour",1);
//		it = new image_transport::ImageTransport(nh);
		image_subscriber = nh.subscribe("/image", 1, &Image_Publisher_Subscriber::on_image_received, this);
		bool_subscriber = nh.subscribe("/bool", 1, &Image_Publisher_Subscriber::on_bool_received, this);
		life_cycle_state_publisher = nh.advertise <std_msgs::Bool>("/life_cycle_state",1);
//		image_subscriber = nh.subscribe("/image", 1, &Image_Publisher_Subscriber::on_image_received, this);
	}
	void on_bool_received(const std_msgs::BoolConstPtr& msg){
			//this->i = this->i +1;
			//cout << i << endl;

	}

	void on_image_received(const system_messages::ImageMsgConstPtr& msg){
	//	cout << "sagggg\n";
		float start = ros::Time::now().toSec();
		bool image_updated = msg->image_is_prepared;

		if(image_updated == false){
			this->publish(false, cv::Mat());
			return;
		}
		sensor_msgs::Image rgb = msg->rgb;
		cv::Mat image = cv_bridge::toCvCopy(rgb, sensor_msgs::image_encodings::BGR8)->image;
	//	cout << "next\n";
//		cv::imshow("image",image);
//		cv::waitKey(1);
		cv::Mat contour_image;
		bool contour_found = this->calc_contours(image, contour_image);
		this->publish(contour_found, contour_image);
		cout<< "Time = "<< ros::Time::now().toSec()-start<<endl;
	}

	bool check_first_frame(Mat thresh){
		
		cv::resize(thresh, thresh, cv::Size(30,30));
		
		vector<vector<Point> > contours;
  		vector<Vec4i> hierarchy;
		cout << "shit the fuck\n";	
		findContours( thresh.clone(), contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
		if(contours.size() == 0){
			return false;
		}
		vector<vector<Point> > contours_poly( contours.size() );
  		vector<Rect> boundRect( contours.size() );
  		vector<Point2f>center( contours.size() );
  		vector<float>radius( contours.size() );
		cout << "next fuck\n";
		//cout << contours.size() << endl;
		for( size_t i = 0; i < contours.size(); i++){
    			approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true );
    			boundRect[i] = boundingRect( Mat(contours_poly[i]) );
    			minEnclosingCircle( contours_poly[i], center[i], radius[i] );
  		}
  		int best_x = 0 , best_y = 0 , best_w = 0 , best_h = 0;
  		int width = thresh.cols , height = thresh.rows;
		
		cout << "khar!\n";
  		for (int i = 0 ; i < boundRect.size() ; i++){
  			cv::Rect rect = boundRect[i];
  			int w = rect.width , h = rect.height , x = rect.x , y = rect.y;
  			if(w  > 4 * width /5){
            			continue;
            		}
            if(x < width/5 || x > 4*width/5 || x + w < width/5 || x+w > 4*width/5)
            	continue;
            if( y < width/5 || y + h < width/5 || y+h > 4*height/5)
                continue;
	        if (w*h < 5)
	        	continue;
            if(w*h > best_w*best_h){
            	best_x = x , best_y = y , best_w = w, best_h = h;
            }
  		}
  		if (best_w*best_h != 0){
  			return true;
  		}
  		return false;
	}

	// void on_image_received(const sensor_msgs::ImageConstPtr& msg){
	// 	std::cout << "yesssssssss!!!!!!!!!!!!!!!!!!" << std::endl;
	// 	cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
	// 	cv::Mat image  = cv_ptr->image;
	// 	Mat contour;
	// 	cv::imshow("rgb",image);
	// 	cv::waitKey(NULL);
	// 	bool has_contour = this->calc_contours(image,contour);
	// 	this->publish(has_contour , contour);
	// }

	bool calc_contours(Mat image, Mat &contour){
		
		// algorithm
		cv::Mat gray;
		cv::cvtColor(image, gray , CV_BGR2GRAY);
		threshold( gray, gray, 100, 255,cv::THRESH_BINARY_INV);
		//adaptiveThreshold(gray, gray, 255,CV_ADAPTIVE_THRESH_MEAN_C,THRESH_BINARY_INV, 35, 2);
		cv::imshow("thresh", gray);
		cv::waitKey(1);
		//cv::imshow("gray",gray);
		//cv::waitKey(1);
		bool valid_contour = this->check_first_frame(gray);
		if(valid_contour == false){
	//		std::cout << "fallllse!\n";
			return false;
		}
		vector<vector<Point> > contours;
  		vector<Vec4i> hierarchy;
		
		findContours( gray.clone(), contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
		if(contours.size() == 0){
			return false;
		}
		vector<vector<Point> > contours_poly( contours.size() );
  		vector<Rect> boundRect( contours.size() );
  		vector<Point2f>center( contours.size() );
  		vector<float>radius( contours.size() );

		for( size_t i = 0; i < contours.size(); i++){
	    		approxPolyDP( Mat(contours[i]), contours_poly[i], 3, true);
    			boundRect[i] = boundingRect( Mat(contours_poly[i]));
    			minEnclosingCircle( contours_poly[i], center[i], radius[i]);
  		}

  		int best_x = 0 , best_y = 0 , best_w = 0 , best_h = 0;
  		int height = gray.rows , width = gray.cols;
//		std::cout << "size  == " << boundRect.size() << std::endl;
		for (int i = 0 ; i < boundRect.size() ; i++){
			Rect rect = boundRect[i];
			int x = rect.x, y = rect.y, w = rect.width, h = rect.height;
//			cout << x << "    " << y << "     " << w << "     " << h << endl;
			if(w  > 2 * width /3){
				//cout << "1\n";
				continue;
			}
			if(x < 10 || x > width -10 || x + w < 10 || x+w > width -10){
				//cout << "2\n";
				continue;
			}
			if( y < 10 || y + h < 10 || y+h > height - 20){
				//cout << "3\n";
				continue;
			}
			if (w*h < 20){
				//cout << "4\n";
				continue;
			}
			if(w*h > best_w*best_h){
				best_x  = x, best_y = y , best_w = w, best_h = h;
			}
		}
	//	cout << "nnanananan\n";
		bool contour_found = false;
	//	cout << best_w << "   best " << best_h << endl;
		if(best_w > 30 && best_h > 30){
			cout << "1\n";
			best_w = best_w + 40, best_h = best_h + 40;
			if ( best_x + best_w > width-1 )
				best_w = width-1 - best_x;
			if ( best_y + best_h > height-1 )
				best_h = height-1 - best_y; 
			best_x = std::max(best_x - 20 , 0) , best_y  = std::max(best_y -20 , 0);
//			cout << best_x << "   " << best_y << "   " << best_x << "     " << best_h << endl;
			cv::Rect roi(best_x,best_y,best_w,best_h);
			cout << "2\n";
			Mat crop_img = image(roi);
			cout << "3\n";
			contour = crop_img;
			cv::imshow("croped", contour);
			cv::waitKey(1);
			contour_found = true;
			return true;
		}
		return false;
	}

	void publish(bool has_contour , Mat contour){
//		std::cout << has_contour << "  = has_contour\n";
		if(has_contour == false){
			std_msgs::Bool life_cycle_ended;
			life_cycle_ended.data = true;
			life_cycle_state_publisher.publish(life_cycle_ended);
			return;
		}
		system_messages::ImageMsg::Ptr contour_msg = boost::make_shared<system_messages::ImageMsg>();
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
//    ros::Subscriber image_subscriber = nh.subscribe("/image", 1, on_image_received);
    ros::spin();
}

